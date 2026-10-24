# Object-Oriented Python: the practical notebook

Original study material by Privatus Cosmas (Priver), depriver.tech.
80 pages, 24 lessons, 48 runnable lesson scripts, a complete lending project,
and 16 capstone tests. Beginner OOP through advanced Python mechanisms.

## Existing authoring conventions followed

Reviewed the existing `studio/python-series/README.md`, series layout and
lesson sources, Python notebook sources, software-architecture README and
content, `docs/docs-archive.md`, and `src/data/archive.ts`.

- Reuse the cream ruled-paper design, green accent, Patrick Hand headings,
  Poppins prose and Liberation Mono code; embed fonts and preserve searchable text.
- Organise each lesson as Learn, Practise, then an explained Solution.
- Include a goal, concrete example, reasoning, common mistake, acceptance
  criteria, hint and extension. Leave worksheet space for predictions.
- Keep runnable code in a companion ZIP and provide an editable Markdown edition.
- Reject overflowing pages and code below the existing minimum font size.
- Execute examples before release, render all pages and inspect the result.
- Reference existing books by their verified local archive filenames; do not
  invent chapter numbers. Add primary Python documentation for deeper study.
- Integrate through the existing static archive catalogue and preview route.

## Build

Use Python with ReportLab and Pillow; Poppler provides `pdftoppm`.
Learners need only Python's standard library for the practice kit.

```sh
python studio/python-oop/build.py
python studio/python-oop/render.py
npm run build
node scripts/check-seo.mjs
```

`content.py` is the editable lesson source. `layout.py` adapts the existing
Python series renderer. `build.py` adds four study/reference pages, executes
all lesson scripts and capstone tests, then creates the PDF and ZIP.
`capstone.py` and `test_capstone.py` are the complete project and its tests.
`verification.json` records actual interpreter and test results.

## Outputs

- `public/archive/python-oop.pdf`
- `public/archive/python-oop-practice.zip`
- `public/archive/previews/python-oop.webp`
- Delivery copies in `/home/priver/Downloads/output/`

## Validation: 24 October 2026

- Python 3.13.15: all 48 lesson scripts executed successfully in separate processes.
- All 16 capstone unit tests passed, including rejected transitions, state
  preservation, independent libraries and defensive snapshots.
- 80 PDF pages rendered and visually reviewed on five contact sheets;
  descriptor and book-reference pages also inspected individually.
- Layout guards passed; every page has the expected page number; all 24
  contents links are present; ZIP integrity checks passed.
- Astro build, publishing-media generation and SEO checks passed.
- Archive metadata, PDF, practice ZIP and preview are prepared locally.
  Nothing from this task has been deployed or pushed.

Python 3.11-compatible syntax is used; only Python 3.13.15 was executed.
There is no claim of type-checker validation, real external delivery, database
transactions, concurrency safety or production-readiness. The source website
was inaccessible through the web tool; references were checked against the
existing local book sources and archive catalogue instead.
