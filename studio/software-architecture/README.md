# Software Architecture: the practical fieldbook

84 pages, 24 chapters. Original realistic teaching scenarios by Privatus Cosmas
(Priver), depriver.tech. Cases and workloads are explicitly illustrative.

## Build

Use a Python environment with ReportLab and Pillow. Poppler is required for QA.

```sh
python -m unittest discover -s studio/software-architecture/practice -v
python studio/software-architecture/build.py
python studio/software-architecture/render.py
```

`content.py` stores original chapter prose, case comparisons and worked answers.
`references.py` maps source keys to primary documentation or original authors.
`build.py` produces the PDF, text edition and practice ZIP.
`render.py` renders all 84 pages, seven contact sheets and the archive cover.

## Validation

- 16 Python/SQLite lab tests passed on Python 3.14.7.
- Demo output: 2 deliveries, 1 new fulfilment, next safe offset 11,
  payment_unknown after timeout.
- Real Kafka commands are an optional documented exercise, not an executed test.
- The transport model is an in-memory list. The relay supports one worker.
- The state machine is not a durable workflow engine. Broker failover,
  concurrent workers, production load and deployment were not exercised.
- PDF layout guards reject page overflow and undersized code.

Website metadata and its preview are in `src/data/archive.ts` and the common
Docs preview route. The practice description is resource-specific so this
book does not incorrectly advertise the earlier Python books' 40-file kits.

All 84 pages were rendered and visually reviewed on contact sheets. The cover,
Kafka diagrams, saga diagram and glossary were also inspected individually.
Text bounds passed on every page. The archive build and SEO checks passed.
