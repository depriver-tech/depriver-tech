import tempfile
import unittest
from pathlib import Path
from architecture_lab import (connect, setup_producer, setup_consumer, place_order,
                              relay_once, consume, next_commit, transition)

class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.p, self.c = connect(), connect()
        self.addCleanup(self.p.close)
        self.addCleanup(self.c.close)
        setup_producer(self.p)
        setup_consumer(self.c)
        self.messages = []

    def count(self, db, table):
        # table is a hardcoded test identifier, never user input.
        return db.execute('SELECT count(*) FROM ' + table).fetchone()[0]

    def order(self, **kwargs):
        return place_order(self.p, 'O-1', 'key-1', 'router', 1, **kwargs)

    def event(self):
        self.order()
        relay_once(self.p, self.messages.append)
        return self.messages[0]

    def test_atomic_acceptance(self):
        self.order()
        self.assertEqual(self.count(self.p, 'orders'), 1)
        self.assertEqual(self.count(self.p, 'outbox'), 1)
        self.assertEqual(self.p.execute('SELECT remaining FROM stock').fetchone()[0], 1)

    def test_producer_rollback(self):
        with self.assertRaises(RuntimeError):
            self.order(fail_before_commit=True)
        self.assertEqual(self.count(self.p, 'orders'), 0)
        self.assertEqual(self.count(self.p, 'outbox'), 0)
        self.assertEqual(self.p.execute('SELECT remaining FROM stock').fetchone()[0], 2)

    def test_same_request_reuses_order(self):
        self.order()
        result = place_order(self.p, 'different-candidate-id', 'key-1', 'router', 1)
        self.assertEqual(result, 'O-1')
        self.assertEqual(self.count(self.p, 'orders'), 1)
        self.assertEqual(self.p.execute('SELECT remaining FROM stock').fetchone()[0], 1)

    def test_changed_request_conflicts(self):
        self.order()
        with self.assertRaises(ValueError):
            place_order(self.p, 'O-2', 'key-1', 'router', 2)
        self.assertEqual(self.count(self.p, 'orders'), 1)

    def test_stock_cannot_be_negative(self):
        place_order(self.p, 'O-1', 'k1', 'router', 2)
        with self.assertRaises(ValueError):
            place_order(self.p, 'O-2', 'k2', 'router', 1)
        self.assertEqual(self.count(self.p, 'outbox'), 1)
        self.assertEqual(self.p.execute('SELECT remaining FROM stock').fetchone()[0], 0)

    def test_invalid_quantity(self):
        for value in [0, -1, True, 1.5, '1']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                place_order(self.p, 'O-1', 'k1', 'router', value)
        self.assertEqual(self.count(self.p, 'orders'), 0)

    def test_publish_crash_redelivers_one_effect(self):
        self.order()
        with self.assertRaises(RuntimeError):
            relay_once(self.p, self.messages.append, fail_after_publish=True)
        self.assertEqual(self.p.execute('SELECT sent FROM outbox').fetchone()[0], 0)
        relay_once(self.p, self.messages.append)
        self.assertEqual(len(self.messages), 2)
        self.assertEqual([consume(self.c, e) for e in self.messages], [True, False])
        self.assertEqual(self.count(self.c, 'fulfilments'), 1)

    def test_broker_error_keeps_pending(self):
        self.order()
        def unavailable(event):
            raise ConnectionError('Simulated broker outage')
        with self.assertRaises(ConnectionError):
            relay_once(self.p, unavailable)
        self.assertEqual(self.p.execute('SELECT sent FROM outbox').fetchone()[0], 0)

    def test_consumer_rollback(self):
        e = self.event()
        with self.assertRaises(RuntimeError):
            consume(self.c, e, fail_before_commit=True)
        self.assertEqual(self.count(self.c, 'inbox'), 0)
        self.assertEqual(self.count(self.c, 'fulfilments'), 0)
        self.assertTrue(consume(self.c, e))

    def test_changed_event_identity_rejected(self):
        e = self.event()
        consume(self.c, e)
        with self.assertRaises(ValueError):
            consume(self.c, {**e, 'quantity': 2})
        self.assertEqual(self.count(self.c, 'fulfilments'), 1)

    def test_business_duplicate_with_new_event_identity(self):
        e = self.event()
        consume(self.c, e)
        self.assertFalse(consume(self.c, {**e, 'event_id': 'another-envelope'}))
        self.assertEqual(self.count(self.c, 'inbox'), 2)
        self.assertEqual(self.count(self.c, 'fulfilments'), 1)

    def test_unknown_schema_rejected(self):
        e = self.event()
        with self.assertRaises(ValueError):
            consume(self.c, {**e, 'version': 2})
        self.assertEqual(self.count(self.c, 'inbox'), 0)

    def test_deduplication_survives_reopen(self):
        e = self.event()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'consumer.db'
            db = connect(path)
            setup_consumer(db)
            self.assertTrue(consume(db, e))
            db.close()
            db = connect(path)
            try:
                self.assertFalse(consume(db, e))
                self.assertEqual(self.count(db, 'fulfilments'), 1)
            finally:
                db.close()

    def test_commit_does_not_skip_gap(self):
        self.assertEqual(next_commit(10, {10, 12}), 11)
        self.assertEqual(next_commit(10, {10, 11, 12}), 13)
        self.assertEqual(next_commit(10, set()), 10)

    def test_timeout_preserves_uncertainty(self):
        state = transition('reserved', 'timeout')
        self.assertEqual(state, 'payment_unknown')
        self.assertEqual(transition(state, 'settled'), 'confirmed')
        with self.assertRaises(ValueError):
            transition(state, 'released')

    def test_compensation_retry_and_duplicate_success(self):
        state = transition('reserved', 'rejected')
        self.assertEqual(transition(state, 'release_failed'), 'release_pending')
        self.assertEqual(transition(state, 'released'), 'cancelled')
        self.assertEqual(transition('confirmed', 'settled'), 'confirmed')

if __name__ == '__main__':
    unittest.main()
