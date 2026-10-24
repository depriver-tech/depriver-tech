"""Build, execute and package the OOP notebook using the existing series design."""
import json
import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from content import BOOK
import layout

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KIT = HERE / 'generated' / BOOK['slug']
OUT = ROOT / 'public/archive'
DELIVER = Path('/home/priver/Downloads/output')

EXTRAS = [
('Study plan', 'A route you can finish', [
('WEEK 1 / FOUNDATIONS / LESSONS 1-6', 'Allow three or four sessions of 45-60 minutes. Run the Python refresher, create two objects and explain self aloud. Practise independent mutable state and a property with a rejected update. Move on when you can create a class without copying a template.'),
('WEEK 2 / COLLABORATION / LESSONS 7-12', 'Compare composition with inheritance, then write two implementations of one interface. Use a Protocol, explain identity versus equality and build a data class. Milestone: justify whether a new feature needs a function, record, collaborator or subclass.'),
('WEEK 3 / RELIABILITY / LESSONS 13-18', 'Implement a reusable iterable and a context manager. Test successful and rejected state transitions. Inject a clock or sender. Milestone: a deliberate defect must make your test fail, and the repaired implementation must pass.'),
('WEEK 4 / ADVANCED PRACTICE / LESSONS 19-24', 'Trace an MRO, build one descriptor and compare subclass hooks with a metaclass. Complete the lending project and inspect its tests. Advanced mechanisms are recognition tools: you do not need to use all of them in your final project.'),
('YOUR STUDY LOOP', 'Predict, run, explain, change, test. Keep a mistake log with the symptom, cause and corrected mental model. Suggested pacing is flexible; repeat a lesson when you cannot explain why its solution works.')]),
('Glossary', 'The vocabulary, in plain language', [
('OBJECT / CLASS / INSTANCE', 'An object has identity, type and value or state. A class defines a type and its behaviour. An instance is an object of a particular class; classes themselves are objects too.'),
('ATTRIBUTE / METHOD / SELF', 'An attribute is a named value accessed on an object. A method is callable behaviour accessed through a class or instance. self names the instance parameter in an ordinary instance method.'),
('ENCAPSULATION / INVARIANT / ABSTRACTION', 'Encapsulation provides a coherent interface around implementation choices. An invariant is a rule valid state must obey. An abstraction exposes the decisions a caller needs while hiding irrelevant details.'),
('COMPOSITION / INHERITANCE / POLYMORPHISM', 'Composition assembles collaborators. Inheritance derives a class from bases. Polymorphism lets one caller use different implementations of the same behavioural contract.'),
('PROTOCOL / DESCRIPTOR / MRO', 'A typing Protocol describes a structural interface. A descriptor customises attribute operations. The method resolution order determines the class search order used by inheritance and cooperative super calls.'),
('VALUE OBJECT / ENTITY / DEPENDENCY', 'A value object is compared by meaningful values. An entity has a continuing domain identity even as details change. A dependency is a collaborator required to perform work; injection supplies it explicitly.')]),
('Your existing library', 'Read the right book next', [
('PYTHON: THE PRACTICAL NOTEBOOK', 'Foundation bridge for variables, loops, functions, files and tests. Read before lesson 2 if lesson 1 feels unfamiliar.\nhttps://depriver.tech/archive/python-the-practical-notebook.pdf'),
('PYTHON WITH DSA', 'Revisit Lists and copying, Hash maps and counting, and collection costs beside lessons 4, 11, 13 and 22.\nhttps://depriver.tech/archive/python-dsa.pdf'),
('PYTHON FOR BACKEND', 'Continue from lessons 10, 17 and 24 into service boundaries, dependencies and test doubles.\nhttps://depriver.tech/archive/python-backend.pdf'),
('SOFTWARE ARCHITECTURE: THE PRACTICAL FIELDBOOK', 'Extend composition and dependency decisions into modular boundaries, ports and adapters, and data ownership.\nhttps://depriver.tech/archive/software-architecture-fieldbook.pdf'),
('GIT AND AUTOMATION', 'Use Git for small, recoverable study commits and Automation for file-oriented projects.\nhttps://depriver.tech/archive/git-the-practical-notebook.pdf\nhttps://depriver.tech/archive/python-automation.pdf')]),
('Graduation checklist', 'Prove what you understand', [
('BEGINNER CHECKPOINT', 'Without looking back, create a class, instantiate it twice, change one instance and explain why the other is unchanged. Explain self, __init__, class attributes and a mutable default argument.'),
('INTERMEDIATE CHECKPOINT', 'Write two interchangeable collaborators and tests for a rejected operation. Explain when composition is clearer than inheritance. Distinguish == from is and show why a frozen object containing a list is not deeply immutable.'),
('ADVANCED CHECKPOINT', 'Trace Service.__mro__ from lesson 19, explain a descriptor lookup and identify when a metaclass is unnecessary. Describe the limits of slots, annotations, fake adapters and in-memory state under concurrency.'),
('CAPSTONE REVIEW / 20 POINTS', 'Award 0-4 each for domain rules, clear public API, failure-path tests, separation of effects, and a reproducible README. Aim for at least 16 with no missing category. This is a self-review rubric, not a certification or guarantee of production readiness.'),
('NEXT INCREMENT', 'Add due dates with a fixed-clock test, then consider SQLite persistence. Preserve the current public contract or document its change. Define how concurrent lending is rejected atomically before exposing a network API.'),
('PRIMARY REFERENCES FOR FURTHER STUDY', 'Typing protocols: https://docs.python.org/3/library/typing.html#typing.Protocol\nAbstract bases: https://docs.python.org/3/library/abc.html\nTesting: https://docs.python.org/3/library/unittest.html')])]

class OOPNotebook(layout.Notebook):
    def finish(self):
        self.cover()
        self.contents()
        self.setup()
        self.lessons()
        self.references()
        for kind, heading, blocks in EXTRAS:
            self.page(kind)
            self.heading(heading)
            for title, text in blocks:
                self.label(title)
                before = self.y
                self.text(text, size=9.5, leading=15.3, space=13)
                # Make every printed URL clickable, with a separate link rectangle.
                urls = [line for line in text.splitlines() if line.startswith('https://')]
                for index, url in enumerate(urls):
                    y = self.y + 13 + (len(urls)-1-index)*15.3
                    self.c.linkURL(url, (layout.LEFT,y,layout.RIGHT,y+15.3), relative=0)
        assert self.n == 80
        self.c.save()
        shutil.copy2(self.path, DELIVER/'pdf'/self.path.name)


def main():
    KIT.mkdir(parents=True, exist_ok=True)
    layout.companions(BOOK)
    for name in ('capstone.py', 'test_capstone.py'):
        shutil.copy2(HERE/name, KIT/name)
    checks = []
    for script in sorted(KIT.glob('lesson_*.py')):
        result = subprocess.run([sys.executable, str(script)], cwd=KIT, capture_output=True, text=True, timeout=20)
        checks.append(dict(file=script.name, passed=result.returncode == 0, output=(result.stdout+result.stderr).strip()))
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', '.', '-v'], cwd=KIT, capture_output=True, text=True, timeout=20)
    checks.append(dict(file='test_capstone.py', passed=result.returncode == 0, output=(result.stdout+result.stderr).strip()))
    report = dict(python=platform.python_version(), lesson_scripts=48, capstone_tests=16, checks=checks)
    (HERE/'verification.json').write_text(json.dumps(report, indent=2)+'\n')
    assert all(check['passed'] for check in checks), json.dumps([x for x in checks if not x['passed']], indent=2)
    shutil.copy2(HERE/'verification.json', KIT/'verification.json')
    md = KIT/'lesson.md'
    with md.open('a') as stream:
        for kind, heading, blocks in EXTRAS:
            stream.write('\n## '+heading+'\n')
            for title, text in blocks:
                stream.write('\n### '+title+'\n\n'+text+'\n')
        stream.write('\n## Primary references\n'+ '\n'.join(f'- [{title}]({url})' for title,url in BOOK['refs'])+'\n')
    readme = KIT/'README.md'
    readme.write_text(readme.read_text()+'''
## Complete lending project

Run `python capstone.py` for the local demonstration.
Run `python -m unittest discover -s . -v` for 16 capstone tests.
Expected demo:

```
Active loans: {'P1': 'Asha'}
Returned by: Asha
Python available: True
```

Keep all files together: lesson_24_solution.py imports capstone.py.
Do not run examples with `python -O`, which disables plain assert checks.
No packages need installing for practice. The PDF builder separately needs
ReportLab; learners do not need that builder to study this book.

This is a single-process, in-memory model. It has no database persistence,
web authentication, concurrent-transaction guarantee or external integrations.
`verification.json` records the interpreter and actual script/test results.
Python 3.11-compatible syntax is used, but only the recorded interpreter was tested.

## Project contract

Book code identifies one physical copy. Codes and titles are stripped and
must be non-empty strings. add() rejects duplicate codes. Unknown codes raise
KeyError. A conflicting loan or invalid return raises LoanError. Invalid
borrower text raises ValueError. Rejected operations preserve existing loans.
active_loans() returns a defensive snapshot. Separate Library objects do not
share state. Book records are frozen; UI and storage remain separate concerns.
''')
    OOPNotebook(BOOK).finish()
    with zipfile.ZipFile(OUT/'python-oop-practice.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(KIT.iterdir()):
            if path.is_file():
                archive.write(path, 'python-oop/'+path.name)
    shutil.copy2(OUT/'python-oop-practice.zip', DELIVER/'python-oop-practice.zip')
    shutil.copy2(md, DELIVER/'python-oop-study-guide.md')
    print('Built 80 pages; 48 lesson scripts and 16 capstone tests passed on Python '+platform.python_version())

if __name__ == '__main__':
    main()
