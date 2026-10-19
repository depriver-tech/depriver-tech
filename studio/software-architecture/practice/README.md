# Software Architecture: the practical fieldbook

Privatus Cosmas (Priver) / depriver.tech

This kit accompanies the 84-page book. Soko Market and the school, ticketing and
logistics cases are fictional teaching scenarios based on common engineering
problems. Workload numbers are illustrative, not measured company benchmarks.

## Local lab: no packages, accounts or network required

Use Python 3.11 or newer. From this extracted folder:

```sh
python architecture_lab.py
python -m unittest test_architecture_lab -v
```

Expected demo output:

```text
Deliveries: 2; new fulfilments: 1
Next safe offset: 11
After a payment timeout: payment_unknown
```

The 16 tests check atomic order/outbox creation, rollback, request identity
conflicts, stock limits, duplicate delivery, consumer rollback, durable
redelivery after reopening SQLite, offset gaps and saga transitions.

The suite was executed on Python 3.14.7. This is a local model: the transport is
an in-memory list, not Kafka. The producer and consumer use separate SQLite
connections. The relay supports one worker and no concurrent claiming.
The saga is a pure state-transition model, not a durable workflow engine.
Real broker failover, TLS, ACLs, concurrency, deployment and load were not tested.

## Experiments

1. In a copy, move the consumer inbox insert after the commit. Predict the
   crash gap this would introduce; do not deploy this broken variation.
2. Add a test for an accepted publish call whose response is lost.
3. Add a saga policy for settlement after reservation expiry. Decide whether
   to reserve again or refund; keep an explicit manual-recovery state.
4. Rebuild a projection from the sample events and compare duplicate handling.
5. Fill in adr-template.md for your own application.

Read kafka-lab.md for an optional real-broker exercise. It is documented from
Apache's tools but was not executed in the authoring environment.
