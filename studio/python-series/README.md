# Python practical notebook series

Five independent 64-page books by Privatus Cosmas (Priver). Each has 20 lessons,
with a learn page, a practice worksheet and an explained solution. Prerequisites
are stated on page 3; absolute beginners should start with the existing 36-page
Python practical notebook. These books are guided foundations, not exhaustive
references to every Python application.

## Sources and outputs

- `dsa.py`, `web.py`, `ai_ml.py`, `backend.py`, `automation.py`: original lesson content.
- `build.py`: ReportLab layout, PDF generation, text editions and companion ZIPs.
- `verify.py`: execute all 200 example/solution scripts, independently.
- `render.py`: render every page and create contact sheets and website covers.
- `manifest.json`: page/lesson/code-file counts.
- `verification.json`: latest individual execution results.
- `public/archive/python-{dsa,web,ai-ml,backend,automation}.pdf`: released books.
- Corresponding `-practice.zip`: 40 Python files, README and text edition per book.

Use a virtual environment with ReportLab, Pillow, Flask, NumPy, FastAPI, Pydantic,
httpx and uvloop (Linux/macOS) installed. Poppler supplies `pdfinfo`, `pdftotext`
and `pdftoppm`. Set `SERIES_FLASK_PYTHON` if Flask lives in a different interpreter. Run `verify.py`, then `build.py`, then `render.py`. Inspect the
rendered pages before publishing changes. Generated source copies and raster
contact sheets are not versioned.

## Validation, 19 October 2026

200/200 scripts passed. Flask examples ran on Python 3.14.7 / Flask 3.1.3.
Other examples ran on Python 3.13.15; relevant packages: NumPy 2.5.3,
FastAPI 0.141.1, Starlette 1.7.0, Pydantic 2.13.5, httpx 0.28.1.
FastAPI TestClient scripts used a uvloop 0.22.1 runner bootstrap because this
restricted environment's default loop stalled when waking client threads.
Published snippets were otherwise executed unchanged. The latest Starlette
emits an httpx deprecation warning; these requests and assertions still passed.

All 320 pages were rendered and reviewed on contact sheets; cover and dense
code pages were also inspected individually. The generator rejects overflowing
paragraphs and undersized code. The website build and SEO checks passed.

This checks the local educational fixtures. Browser execution, real network
integrations, production deployment, and Python 3.11 compatibility were not
executed. The examples use Python 3.11-compatible syntax, but this does not mean
every future package release supports that interpreter. Use a currently
supported Python release with compatible package versions.
