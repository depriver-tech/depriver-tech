# Python notebook source

Rebuild with a Python environment containing ReportLab:

```sh
python build.py
python verify.py
```

Run these commands from this directory, or use the full script paths.
The builder resolves paths relative to itself and uses the repository's licensed fonts.
It produces a searchable 36-page PDF with bookmarks and clickable source links,
plus a Markdown companion and an example manifest. The verifier produces the practice ZIP.

Validation: 18 standard-library examples executed on Python 3.13.15; three foundational
unit tests and two project tests passed. CLI checks cover initial state, persistence,
invalid amounts, empty categories and malformed stored amounts. The optional FastAPI
and pandas examples were checked against official documentation but not executed here.
All 36 pages were rendered with Poppler and reviewed; the cover and project code
were also inspected at a larger scale. Layout guards reject overflowing content.

The handbook is a beginner foundation and major-use-case survey, not an exhaustive
reference for every Python application domain. Existing Python Daily remains available.
