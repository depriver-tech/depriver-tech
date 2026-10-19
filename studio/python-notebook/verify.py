"""Execute offline examples and verify the companion project in a temporary folder."""
from pathlib import Path
import ast
import json
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BUNDLE = HERE / 'practice'
BUNDLE.mkdir(exist_ok=True)
examples = json.loads((HERE/'examples.json').read_text())
for i, (title, code) in enumerate(examples, 1):
    file = BUNDLE / f'lesson_{i:02d}_example.py'
    file.write_text('# '+title+'\n'+code+'\n')
    with tempfile.TemporaryDirectory() as folder:
        subprocess.run([sys.executable, str(file)], cwd=folder, check=True,
                       capture_output=True, text=True)
# Extract exact code used in the PDF so the downloadable project cannot drift.
sections = {}
section = ''
for statement in ast.parse((HERE/'build.py').read_text()).body:
    if not isinstance(statement, ast.Expr) or not isinstance(statement.value, ast.Call):
        continue
    call = statement.value
    if not isinstance(call.func, ast.Name):
        continue
    if call.func.id == 'new' and call.args and isinstance(call.args[0], ast.Constant):
        section = call.args[0].value
    if call.func.id == 'code' and isinstance(call.args[0], ast.Constant):
        sections.setdefault(section, []).append(call.args[0].value)
project = sections['20 / Project: expense notebook'][0] + '\n\n' + sections['21 / Project: make it usable'][0]
(BUNDLE/'expenses.py').write_text(project+'\n')
(BUNDLE/'test_expenses.py').write_text(sections['22 / Project: verify & extend'][0]+'\n')
(BUNDLE/'README.md').write_text('''# Python: the practical notebook - practice files
By Privatus Cosmas (Priver), depriver.tech.

Use Python 3.11 or newer. These files need no third-party packages.
Open a terminal in this folder. On Windows use `py` if `python` is unavailable;
on macOS/Linux use `python3` outside an activated virtual environment.

Run the numbered examples individually: `python lesson_01_example.py`.
The file example creates or overwrites practice_output/notes.txt in your working folder.
The testing example defines tests; run it with `python -m unittest lesson_16_example -v`.

## Expense project
Start in a fresh extracted folder, without an expenses.csv file:

```text
python expenses.py total
python expenses.py add food 3000
python expenses.py add travel 1500
python expenses.py total
python -m unittest test_expenses -v
```

Expected: zero initially, two Saved messages, then Total: 4500 TZS.
The CSV persists next to expenses.py. Repeating add creates another record.
Use only fictional data for practice. See PDF pages 22-24 for explanation and limits.
Optional FastAPI and pandas examples are in the PDF and require separate dependencies.
''')
# Correct the test module reference from the generated lesson ordering.
test_module = next(f'lesson_{i:02d}_example' for i,(title,_) in enumerate(examples,1) if title.startswith('17 /'))
p=BUNDLE/'README.md';p.write_text(p.read_text().replace('lesson_16_example', test_module))
with tempfile.TemporaryDirectory() as folder:
    folder=Path(folder)
    for name in ['expenses.py','test_expenses.py']:
        (folder/name).write_text((BUNDLE/name).read_text())
    def run(*args):
        return subprocess.run([sys.executable,*args],cwd=folder,capture_output=True,text=True)
    assert run('expenses.py','total').stdout.strip() == 'Total: 0 TZS'
    assert run('expenses.py','add','food','3000').returncode == 0
    assert run('expenses.py','add','travel','1500').returncode == 0
    assert run('expenses.py','total').stdout.strip() == 'Total: 4500 TZS'
    before=(folder/'expenses.csv').read_bytes()
    for category,amount in [('food','-1'),('food','0'),('','100'),('food','oops')]:
        assert run('expenses.py','add',category,amount).returncode != 0
        assert (folder/'expenses.csv').read_bytes() == before
    tests=run('-m','unittest','test_expenses','-v')
    assert tests.returncode == 0, tests.stderr
    (folder/'expenses.csv').write_text('category,amount\nfood,invalid\n')
    assert run('expenses.py','total').returncode != 0
with tempfile.TemporaryDirectory() as folder:
    # unittest accepts absolute file paths when the module is importable; use discovery for portability.
    result=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(BUNDLE),'-p',f'{test_module}.py','-v'],capture_output=True,text=True)
    assert result.returncode == 0, result.stderr
out=ROOT/'public/archive/python-notebook-practice.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as archive:
    for file in sorted(BUNDLE.glob('*')):
        if file.is_file(): archive.write(file,'python-notebook-practice/'+file.name)
print(f'{len(examples)} offline examples executed; unit tests and CLI persistence/invalid-input checks passed.\n{out}')
