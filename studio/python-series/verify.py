"""Execute all standalone teaching examples with local dependency environments."""
import ast, importlib, json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BOOKS = ['dsa', 'web', 'backend', 'ai_ml', 'automation']
PYTHON = os.environ.get('SERIES_PYTHON', sys.executable)
FLASK_PYTHON = os.environ.get('SERIES_FLASK_PYTHON', PYTHON)
results = []
for name in BOOKS:
    book = importlib.import_module(name).BOOK
    for number, lesson in enumerate(book['lessons'], 1):
        for kind, key in [('example', 'code'), ('solution', 'solution')]:
            code = lesson[key]
            label = f'{name}/{number:02d}_{kind}'
            try:
                ast.parse(code)
                interpreter = FLASK_PYTHON if 'from flask' in code else PYTHON
                # The sandbox's default event loop cannot wake TestClient threads.
                # uvloop changes the test runner, not the published lesson.
                bootstrap = 'import uvloop; uvloop.install()\n' if 'from fastapi.testclient' in code else ''
                run = subprocess.run([interpreter, '-c', bootstrap + code], text=True, capture_output=True, timeout=15)
                result = dict(label=label, passed=run.returncode == 0, interpreter=interpreter,
                              stderr=run.stderr if run.returncode else '')
            except Exception as error:
                result = dict(label=label, passed=False, stderr=str(error))
            results.append(result)
            if not result['passed']:
                print(label, result['stderr'])
(ROOT/'verification.json').write_text(json.dumps(results, indent=2)+'\n')
print(f"{sum(x['passed'] for x in results)}/{len(results)} snippets passed")
sys.exit(any(not x['passed'] for x in results))
