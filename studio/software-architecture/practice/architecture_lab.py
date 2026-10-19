"""Local teaching model: SQLite outbox and inbox, simulated transport, saga rules.

No Kafka or network calls. Databases are supplied by the caller. Not a production
relay: there is no multi-worker claim, retry scheduler, authentication or monitoring.
"""
import json
import sqlite3


def connect(path=':memory:'):
    db = sqlite3.connect(path)
    db.execute('PRAGMA foreign_keys=ON')
    return db


def setup_producer(db):
    db.executescript('''
    CREATE TABLE stock(sku TEXT PRIMARY KEY, remaining INTEGER NOT NULL
                       CHECK(remaining >= 0));
    CREATE TABLE orders(id TEXT PRIMARY KEY, request_key TEXT UNIQUE NOT NULL,
                        fingerprint TEXT NOT NULL, sku TEXT NOT NULL,
                        quantity INTEGER NOT NULL CHECK(quantity > 0));
    CREATE TABLE outbox(id TEXT PRIMARY KEY, payload TEXT NOT NULL,
                        sent INTEGER NOT NULL DEFAULT 0 CHECK(sent IN (0,1)));
    INSERT INTO stock VALUES ('router', 2);
    ''')


def setup_consumer(db):
    db.executescript('''
    CREATE TABLE inbox(id TEXT PRIMARY KEY, payload TEXT NOT NULL);
    CREATE TABLE fulfilments(order_id TEXT PRIMARY KEY, sku TEXT NOT NULL,
                             quantity INTEGER NOT NULL CHECK(quantity > 0));
    ''')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def place_order(db, order_id, request_key, sku, quantity, fail_before_commit=False):
    if not all(isinstance(x, str) and x for x in (order_id, request_key, sku)):
        raise ValueError('Identifiers must be non-empty strings')
    if type(quantity) is not int or quantity <= 0:
        raise ValueError('Quantity must be a positive integer')
    fingerprint = canonical({'sku': sku, 'quantity': quantity})
    # BEGIN IMMEDIATE serialises SQLite writers for this small demonstration.
    # Call only with a connection that has no active transaction.
    db.execute('BEGIN IMMEDIATE')
    try:
        prior = db.execute('SELECT id, fingerprint FROM orders WHERE request_key=?',
                           (request_key,)).fetchone()
        if prior:
            if prior[1] != fingerprint:
                raise ValueError('Idempotency key reused for a different request')
            db.commit()
            return prior[0]
        changed = db.execute('''UPDATE stock SET remaining=remaining-?
            WHERE sku=? AND remaining>=?''', (quantity, sku, quantity)).rowcount
        if changed != 1:
            raise ValueError('Insufficient stock or unknown item')
        db.execute('INSERT INTO orders VALUES (?,?,?,?,?)',
                   (order_id, request_key, fingerprint, sku, quantity))
        event = {'event_id': 'placed:' + order_id, 'type': 'OrderPlaced',
                 'version': 1, 'order_id': order_id, 'sku': sku,
                 'quantity': quantity}
        db.execute('INSERT INTO outbox(id,payload) VALUES (?,?)',
                   (event['event_id'], canonical(event)))
        if fail_before_commit:
            raise RuntimeError('Injected failure before commit')
        db.commit()
        return order_id
    except BaseException:
        db.rollback()
        raise


def relay_once(db, publish, fail_after_publish=False):
    """One relay only. Publish may accept data and still raise (lost response)."""
    row = db.execute('SELECT id,payload FROM outbox WHERE sent=0 ORDER BY rowid LIMIT 1').fetchone()
    if row is None:
        return False
    ident, payload = row
    publish(json.loads(payload))
    if fail_after_publish:
        raise RuntimeError('Injected crash after publish, before sent marker')
    with db:
        db.execute('UPDATE outbox SET sent=1 WHERE id=?', (ident,))
    return True


def consume(db, event, fail_before_commit=False):
    if event.get('type') != 'OrderPlaced' or event.get('version') != 1:
        raise ValueError('Unsupported event contract')
    for key in ('event_id', 'order_id', 'sku'):
        if not isinstance(event.get(key), str) or not event[key]:
            raise ValueError('Missing identity')
    quantity = event.get('quantity')
    if type(quantity) is not int or quantity <= 0:
        raise ValueError('Invalid quantity')
    payload = canonical(event)
    db.execute('BEGIN IMMEDIATE')
    try:
        prior = db.execute('SELECT payload FROM inbox WHERE id=?',
                           (event['event_id'],)).fetchone()
        if prior:
            if prior[0] != payload:
                raise ValueError('Event identity reused with changed payload')
            db.commit()
            return False
        old_effect = db.execute('SELECT sku,quantity FROM fulfilments WHERE order_id=?',
                                (event['order_id'],)).fetchone()
        effect = (event['sku'], quantity)
        if old_effect and old_effect != effect:
            raise ValueError('Conflicting business duplicate')
        if not old_effect:
            db.execute('INSERT INTO fulfilments VALUES (?,?,?)',
                       (event['order_id'], *effect))
        db.execute('INSERT INTO inbox VALUES (?,?)', (event['event_id'], payload))
        if fail_before_commit:
            raise RuntimeError('Injected failure before consumer commit')
        db.commit()
        return old_effect is None
    except BaseException:
        db.rollback()
        raise


def next_commit(start, completed):
    """Next offset after the contiguous completed prefix, not max(completed)+1."""
    while start in completed:
        start += 1
    return start


TRANSITIONS = {
    ('reserved', 'timeout'): 'payment_unknown',
    ('reserved', 'settled'): 'confirmed',
    ('payment_unknown', 'settled'): 'confirmed',
    ('reserved', 'rejected'): 'release_pending',
    ('payment_unknown', 'rejected'): 'release_pending',
    ('release_pending', 'release_failed'): 'release_pending',
    ('release_pending', 'released'): 'cancelled',
    ('confirmed', 'settled'): 'confirmed',
    ('cancelled', 'released'): 'cancelled',
}


def transition(state, event):
    """Pure model, not durable workflow storage; assumes a still-valid reservation."""
    try:
        return TRANSITIONS[state, event]
    except KeyError as error:
        raise ValueError('Transition requires an explicit business policy') from error


if __name__ == '__main__':
    producer, consumer = connect(), connect()
    setup_producer(producer)
    setup_consumer(consumer)
    messages = []  # Simulated transport, not a durable broker.
    place_order(producer, 'O-42', 'checkout-42', 'router', 1)
    try:
        relay_once(producer, messages.append, fail_after_publish=True)
    except RuntimeError:
        pass
    relay_once(producer, messages.append)
    effects = sum(consume(consumer, event) for event in messages)
    print(f'Deliveries: {len(messages)}; new fulfilments: {effects}')
    print('Next safe offset:', next_commit(10, {10, 12}))
    print('After a payment timeout:', transition('reserved', 'timeout'))
    producer.close()
    consumer.close()
