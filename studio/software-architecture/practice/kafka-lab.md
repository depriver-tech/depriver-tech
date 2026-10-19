# Optional Kafka broker exercise

This exercise was checked against Apache's documentation but **not executed**
in the authoring environment. The required network/runtime access was not
available. It is separate from the tested Python/SQLite model.

Use a disposable local Kafka installation following the official quickstart:
https://kafka.apache.org/quickstart/

The documentation checked for this edition uses Kafka 4.3.1; its downloaded
script path requires Java 17 or newer. Follow the version-matched quickstart
for startup. Do not expose a learning broker publicly. These commands assume
an already running broker at localhost:9092 and a terminal in the extracted
Kafka distribution. They use a new topic called architecture-orders-lab.

## 1. Create a three-partition topic

```sh
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create \
  --topic architecture-orders-lab --partitions 3 --replication-factor 1
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe \
  --topic architecture-orders-lab
```

Replication factor one is for this local demonstration only. Expect three
partition descriptions; this does not demonstrate replicated durability.

## 2. Publish keyed records

```sh
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic architecture-orders-lab \
  --property parse.key=true --property key.separator=:
```

Enter these lines, then stop the producer with Ctrl-C:

```text
O-42:OrderPlaced
O-42:PaymentSettled
O-43:OrderPlaced
```

The console values are deliberately simple strings, not production event
schemas. Under the unchanged default keyed partitioning setup, the O-42
records should go to the same partition. Do not predict the partition number
from Python's built-in hash: it is not Kafka's partitioner.

## 3. Read with a named group

```sh
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic architecture-orders-lab --group architecture-a --from-beginning \
  --property print.key=true --property print.partition=true \
  --property print.offset=true
```

Observe the partition and offset for each record. Ordering is within each
partition, not a single total order across all printed records.

Start another consumer with the same group in a different terminal, then
publish more records. Inspect assignments while both consumers are running:

```sh
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group architecture-a
```

Use a different group, architecture-b, to observe independent progress.
`--from-beginning` affects where a group without valid committed progress
starts; it does not override existing committed offsets. Use a new group
identity for this replay exercise instead of assuming the flag rewinds it.

## 4. Review

- Which partition contains both O-42 records?
- How does the same-group assignment differ from a new independent group?
- What must an email consumer do before replaying real events?
- Why do these console observations not prove exactly-once external effects?

Stop the consumers and the disposable broker using the startup method's
instructions. Delete only resources created for this lab when no longer needed.
