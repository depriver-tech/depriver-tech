"""Rebuild the searchable, notebook-style Python lesson. Requires reportlab."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'public/archive/python-the-practical-notebook.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
for name,file in [('Hand','PatrickHand-Regular.ttf'),('Body','Poppins-Regular.ttf'),('Bold','Poppins-SemiBold.ttf'),('Code','LiberationMono-Regular.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(ROOT/'studio/fonts'/file)))
INK='#152E56'; BLUE='#244E9A'; PAPER='#FBF7ED'; YELLOW='#F8DD72'
W,H=595.28,841.89
c=canvas.Canvas(str(OUT),pagesize=(W,H)); c.setTitle('Python: The Practical Notebook');c.setAuthor('Privatus Cosmas (Priver)');c.setSubject('Python foundations, practical projects and major use cases')
page=0;y=0
plain=[]

def para(text,size=11,font='Body',color=INK,gap=14):
    global y
    p=Paragraph(escape(text),ParagraphStyle('p',fontName=font,fontSize=size,leading=(size*1.2 if size>=27 else 19),textColor=HexColor(color)))
    _,h=p.wrap(455,700)
    if y-h<82: raise ValueError(f'Page {page} overflow: {text[:35]} at {y}')
    p.drawOn(c,86,y-h);y-=h+gap;plain.append(text+'\n')

def head(text):
    global y
    para(text,22,'Hand',BLUE,8)

def code(text):
    global y
    lines=text.split('\n');h=14*len(lines)+24
    if y-h<82: raise ValueError(f'Code overflow page {page}')
    c.setFillColor(HexColor('#EFF3F8')); c.roundRect(80,y-h,462,h,7,fill=1,stroke=0)
    c.setFillColor(HexColor(INK));c.setFont('Code',9.3)
    for i,line in enumerate(lines):
        if pdfmetrics.stringWidth(line,'Code',9.3)>440: raise ValueError('Code too wide: '+line)
        c.drawString(92,y-19-i*14,line)
    y-=h+16;plain.append('```python\n'+text+'\n```\n')

def note(text):
    global y
    p=Paragraph(escape(text),ParagraphStyle('n',fontName='Hand',fontSize=17,leading=21,textColor=HexColor(INK)))
    _,h=p.wrap(425,700)
    if y-h-24<74: raise ValueError(f'Note overflow {page}')
    c.setFillColor(HexColor('#FAEBA7'));c.roundRect(80,y-h-20,462,h+20,3,stroke=0,fill=1)
    p.drawOn(c,96,y-h-10);y-=h+38;plain.append('Note: '+text+'\n')

def new(title,subtitle,ref=''):
    global page,y
    if page:c.showPage()
    page+=1
    c.setFillColor(HexColor(PAPER));c.rect(0,0,W,H,fill=1,stroke=0)
    c.setStrokeColor(HexColor('#D4E1E9'));c.setLineWidth(.4)
    for line in range(102,760,22):c.line(34,line,W-30,line)
    c.setStrokeColor(HexColor('#DB8D89'));c.line(65,75,65,H-43);c.line(68,75,68,H-43)
    c.setFillColor(HexColor(INK));c.setFont('Code',9);c.drawString(85,H-40,'depriver.tech  /  FIELD NOTES');c.drawRightString(W-35,H-40,'PYTHON / 2026')
    c.setFillColor(HexColor(YELLOW));c.rect(83,H-113,min(440,pdfmetrics.stringWidth(title,'Hand',33)),9,fill=1,stroke=0)
    c.setFillColor(HexColor(INK));c.setFont('Hand',33);c.drawString(84,H-110,title)
    c.setFont('Body',9);c.drawString(85,H-135,subtitle)
    c.setFont('Code',8);c.drawString(85,43,'LEARN IT. TRY IT. KEEP THE NOTES.');c.drawRightString(W-35,43,f'{page:02}')
    if ref:
        c.setFont('Body',6.8);c.drawString(85,62,ref)
        if ref.startswith('https://'):c.linkURL(ref,(85,59,540,70),relative=0)
    c.bookmarkPage(f'p{page}');c.addOutlineEntry(title,f'p{page}',0)
    plain.append('\n# '+title+'\n'+subtitle+'\n');y=H-167


examples=[]
def lesson(title, subtitle, explanation, snippet='', after='', task='', ref='', run=True):
    new(title,subtitle,ref)
    para(explanation)
    if snippet:
        code(snippet)
        if run: examples.append((title,snippet))
    if after: para(after)
    if task: note(task)

new('Python: the practical notebook','Beginner foundations. Useful projects. A map of the possibilities.')
para('Start with one line.\nBuild something useful.',30,'Hand',gap=26)
para('By Privatus Cosmas (Priver) / depriver.tech',12,'Bold')
para('A hands-on handbook for people learning to program: clear explanations, runnable examples, practice prompts and a small command-line project you can finish yourself.')
head('Inside these pages')
para('Learn variables, decisions, loops and functions. Work with files, JSON, CSV and SQLite. Test and debug your code. Then explore automation, web APIs, data analysis, AI, science, desktop apps and more.')
note('Type it. Predict the result. Run it. Change it. Explain it in your own words.')
para('Edition 1.0 / 19 October 2026\nCore examples use Python 3.11 or newer. Optional libraries require their own supported Python versions.',9)
head('A practical foundation, not an encyclopedia')
para('This book surveys the major uses of Python. Each specialist field has more to learn; no single beginner document covers every library or use case.',10)

new('Your learning route','Read in order first; return to individual lessons later')
for t,d in [('01 / Start here - pages 3-5','Install Python, run a script and create a separate environment.'),('02 / Learn the language - pages 6-15','Values, collections, decisions, loops, functions, modules and errors.'),('03 / Work with real data - pages 16-21','Files, CSV, JSON, classes, testing, SQLite and command-line tools.'),('04 / Build a project - pages 22-24','A persistent expense notebook with validation and tests.'),('05 / Explore the uses - pages 25-32','Automation, APIs, analytics, AI, science, creative tools and operations.'),('06 / Keep improving - pages 33-36','Professional habits, exercises with answers, a study plan and sources.')]:
    head(t);para(d,10.5,gap=9)
note('Everything through the core project uses the standard library. Optional web and data examples are clearly labelled.')

lesson('01 / Think like a programmer','A program turns a clear instruction into a repeatable action',
'A program is a sequence of instructions. Input is information it receives; processing is what it does with that information; output is the result. Before writing code, explain the task in everyday language.',
'prices = [1200, 800, 500]\ntotal = sum(prices)\nprint("Total:", total, "TZS")',
'This list holds three prices. sum adds them; print displays Total: 2500 TZS. The equals sign assigns a value to a name. Python executes these statements from top to bottom. A name such as total makes the meaning easier to understand than repeating the calculation everywhere.',
'Practice: add one more price. Predict the new total before running the script.')
head('Break down a larger task')
para('For a spending notebook: accept a category and amount, check that they are valid, save the entry, then show a total. Each step can become a small function. Begin with the smallest useful version; add complexity after it works.')

lesson('02 / Install and run','Terminal commands and Python code belong in different places',
'Install a supported Python 3 release from python.org/downloads or your operating system package manager. Open a terminal. On Windows, try py --version; on macOS or Linux, try python3 --version. Do not use Python 2. Create a folder called python-notebook.',
'# Save this Python code as hello.py\nname = "Priver"\nprint(f"Hello, {name}!")',
'In the terminal, change into the folder with cd and run py hello.py on Windows or python3 hello.py on macOS/Linux. Expected output: Hello, Priver! A .py file is a script. The interactive prompt is useful for quick experiments, but save repeatable work in files.',
'If Python cannot find hello.py, check your current folder and the exact filename. Avoid saving it as hello.py.txt.')
head('Read the notation')
para('Text after # is a comment. Quoted text is a string. Parentheses call a function. Examples in blue boxes are Python unless explicitly labelled as terminal commands. Never copy the >>> prompt from a tutorial into a script.')

lesson('03 / Keep projects separate','A virtual environment holds one project\'s installed packages',
'Create an environment inside the project folder. Use python3 on macOS/Linux or py on Windows for the creation command. After activation, this book uses python to mean the environment interpreter.',
'# Terminal: macOS / Linux\npython3 -m venv .venv\nsource .venv/bin/activate\npython --version\n\n# Terminal: Windows Command Prompt\npy -m venv .venv\n.venv\\Scripts\\activate.bat\npython --version',
'Use the commands for your operating system, not both sets. In PowerShell, activation is .venv\\Scripts\\Activate.ps1. If policy blocks activation, invoke .venv\\Scripts\\python.exe directly. On some Linux systems you need the distribution\'s python3-venv package first.',
'Add .venv/ and __pycache__/ to .gitignore. Recreate environments from dependency records instead of committing them.',ref='https://docs.python.org/3/library/venv.html',run=False)

lesson('04 / Values and names','Choose the right kind of value for the job',
'An int holds a whole number, a float represents an approximate real number, a str holds text and a bool is True or False. None represents the absence of a value. Python names refer to objects; assignment does not declare a permanently fixed type.',
'quantity = 3\nprice = 1500\nitem = "Notebook"\navailable = True\ntotal = quantity * price\nprint(item, total)\nprint(type(quantity).__name__)\nprint(7 / 2, 7 // 2, 7 % 2)\nprint(2 ** 3)',
'Output: Notebook 4500, then int, then 3.5 3 1, then 8. / divides; // uses floor division; % gives a remainder; ** raises to a power. Use descriptive snake_case names such as total_cost. Avoid naming a variable list or str because that hides a built-in name.',
'For these money exercises use whole TZS integers. For exact fractional money, use Decimal with a documented rounding rule.')

lesson('05 / Text and user input','Input arrives as text until you convert it',
'String methods return useful transformed values. strip removes surrounding whitespace; lower normalises letter case. An f-string inserts values into text. Indexing starts at zero; slices stop before their end position.',
'name = "  Asha  "\nclean = name.strip()\nprint(f"Hello, {clean}!")\nprint(clean[0], clean[:2])\nprint("python".upper())\nprint("web,data,ai".split(","))',
'Expected: Hello, Asha!; A As; PYTHON; then a list of three words. A string is immutable: clean.upper() does not change clean unless you assign the returned value. input("Your age: ") returns a string; int(...) converts suitable text to a whole number.',
'Practice: clean "  MBEYA  " into "Mbeya" with strip and title. Predict what int("two") does; we handle that error on page 15.')

lesson('06 / Make decisions','Use conditions to choose the next action',
'An if block runs when its condition is true. elif checks another possibility; else handles what remains. Indent the body consistently with four spaces. Comparisons include ==, !=, <, <=, > and >=. = assigns; == compares.',
'budget = 5000\ncost = 4200\nif cost < 0:\n    print("Invalid cost")\nelif cost <= budget:\n    print("Within budget")\nelse:\n    print("Over budget")\n\nis_member = True\nprint(is_member and cost <= budget)',
'This prints Within budget and True. and requires both conditions; or needs at least one; not reverses a truth value. Empty lists, empty strings, zero and None are false-like in conditions. Prefer explicit checks when zero is a valid value.',
'Practice: try cost = 6000, cost = -1 and cost = 5000. Explain why the order of the conditions matters.')

lesson('07 / Lists and tuples','Keep related values in an ordered collection',
'A list is an ordered, mutable sequence. append adds one item. A tuple is an ordered sequence whose elements cannot be reassigned. Use a list for a growing collection and a tuple for a fixed grouping such as a coordinate.',
'items = ["pen", "book"]\nitems.append("bag")\nprint(items[0], items[-1])\nprint(items[:2])\nprint(len(items))\ncopy = items.copy()\ncopy.append("ruler")\nprint(len(items), len(copy))\nlocation = (-8.9, 33.4)\nlatitude, longitude = location',
'Expected: pen bag, then [\'pen\', \'book\'], then 3 and finally 3 4. items.copy() makes a shallow copy; nested objects are still shared. Writing copy = items would make both names refer to the same list. An out-of-range index raises IndexError.',
'Practice: replace "pen" with "pencil", then remove "bag". Check the list after each operation.')

lesson('08 / Dictionaries and sets','Look up values by meaning rather than position',
'A dictionary maps unique keys to values. A set stores distinct elements and supports membership checks. Dictionary keys and set members must be hashable; strings and integers are common choices.',
'student = {"name": "Asha", "score": 82}\nstudent["city"] = "Mbeya"\nprint(student["name"])\nprint(student.get("phone", "Not supplied"))\nfor key, value in student.items():\n    print(key, value)\n\nskills = {"Python", "SQL", "Python"}\nprint(len(skills))\nprint("SQL" in skills)',
'The dictionary contains three fields. get returns a fallback when a key is absent, while square-bracket lookup raises KeyError. The set has two elements because Python appears only once. Do not rely on a set\'s display order.',
'Practice: model one shop item with name, quantity and price keys. Compute quantity times price.')

lesson('09 / Repeat with loops','Process each item without rewriting the same statement',
'A for loop visits items from an iterable. range(1, 4) produces 1, 2 and 3. enumerate supplies an index and value. A while loop repeats as long as its condition is true; ensure something changes so it can finish.',
'prices = [1000, 2500, 500]\nfor number, price in enumerate(prices, start=1):\n    print(number, price)\n\nremaining = 3\nwhile remaining > 0:\n    print("Attempts:", remaining)\n    remaining -= 1\n\nprint(sum(prices))',
'The first loop prints three numbered prices; the second counts 3, 2, 1; the total is 4000. break leaves a loop immediately. continue skips the rest of one iteration. Prefer iterating directly over values when you do not need their positions.',
'Practice: print only prices above 1000. Then total those prices with a loop before trying sum.')

lesson('10 / Functions that return','Name a small task and reuse it',
'A function groups a task behind a name. Parameters receive inputs; return sends a result to the caller. print only displays information. A function without an explicit return returns None.',
'def line_total(price: int, quantity: int = 1) -> int:\n    if price < 0 or quantity < 0:\n        raise ValueError("Use non-negative values")\n    return price * quantity\n\nfirst = line_total(1500, 3)\nsecond = line_total(price=500)\nprint(first + second)',
'The result is 5000. The default quantity is 1; keyword arguments make calls clearer. Type hints explain intended types but do not enforce them at runtime. Variables assigned inside a function are normally local to it. Keep input/output at the edges and calculations in small functions.',
'Practice: write a function that converts minutes into seconds. Test zero, one and five minutes.')

lesson('11 / Comprehensions & generators','Transform collections clearly; stream larger results',
'A comprehension builds a new collection from an existing iterable. Use it for short transformations; use an ordinary loop when the logic becomes hard to read. A generator yields values on demand instead of building the complete result immediately.',
'prices = [100, 200, 300, 400]\nlarge = [p for p in prices if p >= 300]\nprint(large)\n\ndef squares(limit):\n    for n in range(limit):\n        yield n * n\n\nvalues = squares(4)\nprint(list(values))\nprint(list(values))',
'The output is [300, 400], then [0, 1, 4, 9], then []. A generator is consumed as you iterate over it. Recreate it if you need another pass. A shallow copy of a collection and a generator both have different behaviour from a reusable list.',
'Practice: build a dictionary mapping each number from 1 to 4 to its square.')

lesson('12 / Modules and packages','Split responsibilities into files you can understand',
'A module is importable Python code, often one .py file. A package groups modules. The standard library ships with Python; third-party packages are installed separately. Start with standard modules before adding dependencies.',
'from statistics import mean\nfrom datetime import date\n\nscores = [60, 75, 90]\nprint(mean(scores))\nprint(date(2026, 10, 19).isoformat())\n\ndef main():\n    print("Notebook ready")\n\nif __name__ == "__main__":\n    main()',
'This prints 75, 2026-10-19 and Notebook ready when run as a script. The main guard lets another file import functions without automatically running the application. Put reusable calculations in a module such as totals.py and import them with from totals import line_total.',
'Avoid filenames such as json.py or statistics.py in your project: they can hide the standard-library modules.')

lesson('13 / Errors are information','Read the final error line, then trace back to its cause',
'SyntaxError means Python could not parse the code. NameError often means an undefined name. TypeError means an operation received an unsuitable type. ValueError means a value is invalid for an otherwise appropriate operation.',
'raw = "not a number"\ntry:\n    quantity = int(raw)\nexcept ValueError:\n    print("Enter a whole number")\nelse:\n    print(quantity * 1500)\nfinally:\n    print("Check complete")',
'The output is Enter a whole number and Check complete. Catch only exceptions you know how to handle. Broad except blocks can hide programming mistakes. When debugging, reduce the input, inspect values with repr, and check the first point where reality differs from your expectation.',
'Practice: replace raw with "3". Why does the else block run now? Do not use eval to convert user input.')

lesson('14 / Files and paths','Save information so it survives the next run',
'pathlib represents file paths across operating systems. Use explicit UTF-8 encoding for text. Relative paths are resolved from the current working directory, which may differ from the script\'s directory. This example creates a local practice file and overwrites it on each run.',
'from pathlib import Path\n\nfolder = Path("practice_output")\nfolder.mkdir(exist_ok=True)\npath = folder / "notes.txt"\npath.write_text("Learn Python\\nTry a project\\n",\n                encoding="utf-8")\nwith path.open(encoding="utf-8") as handle:\n    for line in handle:\n        print(line.strip())',
'with closes the file even when an error occurs. Use mode "a" to append and mode "w" to replace contents. Reading line by line is useful for large text files; read_text loads everything into memory. For data beside a script, start from Path(__file__).resolve().parent.',
'Practice: append a third line in your practice folder. Verify that the first two lines remain.')

lesson('15 / CSV and JSON','Exchange structured data with other tools',
'CSV is useful for rows and columns. JSON represents nested dictionaries, lists, strings, numbers, booleans and null. CSV fields arrive as text and need conversion. JSON is data, not executable Python.',
'import csv\nimport io\nimport json\n\nsource = "category,amount\\nfood,3000\\ntravel,1500\\n"\nrows = list(csv.DictReader(io.StringIO(source)))\ntotal = sum(int(row["amount"]) for row in rows)\nreport = {"currency": "TZS", "total": total}\nencoded = json.dumps(report, indent=2)\nprint(encoded)\nprint(json.loads(encoded)["total"])',
'The JSON report contains a total of 4500; the final line prints 4500. json.dumps produces text; loads parses it. For real CSV files use open(..., newline="", encoding="utf-8"). Validate required fields, types and ranges after parsing; valid JSON is not automatically valid business data.',
'Practice: add a third CSV row. Then deliberately remove its amount and decide how your program should report the bad row.')

lesson('16 / Classes and dataclasses','Group state with related behaviour when that helps',
'A class describes a kind of object. An instance is one object of that class. self refers to that instance. A dataclass generates routine methods such as initialisation, making simple records easier to express.',
'from dataclasses import dataclass\n\n@dataclass\nclass Expense:\n    category: str\n    amount: int\n\n    def label(self):\n        return f"{self.category}: {self.amount} TZS"\n\nentry = Expense("food", 3000)\nprint(entry.label())',
'The output is food: 3000 TZS. Each instance has its own field values. Use ordinary functions and dictionaries when they are simpler. Classes are helpful when a concept has state and operations that belong together. Type annotations do not validate the amount; add validation where data enters the system.',
'Practice: create two Expense instances. Change one amount and check that the other instance stays unchanged.')

lesson('17 / Test behaviour','A good test tells you which promise stopped holding',
'Tests make expected behaviour explicit. Test ordinary input, boundary cases and invalid input. The standard library includes unittest. Save the example as test_total.py and run python -m unittest -v from the same folder.',
'import unittest\n\ndef total_amount(amounts):\n    if any(x < 0 for x in amounts):\n        raise ValueError("Negative amount")\n    return sum(amounts)\n\nclass TotalTests(unittest.TestCase):\n    def test_total(self):\n        self.assertEqual(total_amount([2, 3]), 5)\n    def test_empty(self):\n        self.assertEqual(total_amount([]), 0)\n    def test_invalid(self):\n        with self.assertRaises(ValueError):\n            total_amount([-1])',
'Expected: three tests pass. A test that only checks your code against itself proves little. Use known examples and real requirements. Automated tests complement manual checking; they cannot prove that every possible input is correct.',
'Practice: add a zero-value test. Change sum(amounts) to 0 and watch which test catches the mistake.')

lesson('18 / A small database','SQLite stores related records in a local database',
'SQLite is included in Python through sqlite3. A table has rows and columns; SQL selects and updates those rows. This example uses an in-memory database, so it creates no persistent database file.',
'import sqlite3\n\ncon = sqlite3.connect(":memory:")\ntry:\n    con.execute("CREATE TABLE expenses "\n                "(category TEXT, amount INTEGER)")\n    con.execute("INSERT INTO expenses VALUES (?, ?)",\n                ("food", 3000))\n    con.commit()\n    row = con.execute(\n        "SELECT SUM(amount) FROM expenses"\n    ).fetchone()\n    print(row[0])\nfinally:\n    con.close()',
'The result is 3000. Replace :memory: with a filename for persistence. Use placeholders for values instead of inserting user input into SQL text. Commit writes intentionally; close connections when finished. A connection context manager manages transactions but does not itself close the connection.',
'Practice: insert travel = 1500, then query the total again. Expected: 4500.',ref='https://docs.python.org/3/library/sqlite3.html')

lesson('19 / Command-line tools','Turn a script into something you can run with arguments',
'argparse turns terminal arguments into named values and generates --help. Save this script as greet.py. Run python greet.py Asha --times 2. Terminal arguments are separate from interactive input(), which pauses to ask a question.',
'import argparse\n\ndef main():\n    parser = argparse.ArgumentParser()\n    parser.add_argument("name")\n    parser.add_argument("--times", type=int, default=1)\n    args = parser.parse_args()\n    if not 1 <= args.times <= 10:\n        parser.error("--times must be between 1 and 10")\n    for _ in range(args.times):\n        print(f"Hello, {args.name}!")\n\nif __name__ == "__main__":\n    main()',
'Expected: Hello, Asha! appears twice. Try python greet.py --help and python greet.py Asha --times 0. A useful CLI validates input, prints actionable messages and exits with a nonzero status when it cannot complete the task.',
'Practice: add an optional --city argument with default "Mbeya" and include it in the greeting.',run=False)

new('20 / Project: expense notebook','A complete local application / Part 1: the data layer')
para('Create a new folder. Save the code on this page and the next into one file named expenses.py, in that order. The companion ZIP includes the complete file. The app accepts whole positive TZS amounts and stores entries in a CSV beside the script.')
code('import argparse\nimport csv\nfrom pathlib import Path\n\nDATA = Path(__file__).resolve().with_name("expenses.csv")\n\ndef add_expense(path, category, amount):\n    category = category.strip()\n    if not category or amount <= 0:\n        raise ValueError("Category and positive amount required")\n    new_file = not path.exists() or path.stat().st_size == 0\n    with path.open("a", newline="", encoding="utf-8") as f:\n        writer = csv.writer(f)\n        if new_file:\n            writer.writerow(["category", "amount"])\n        writer.writerow([category, amount])\n\ndef total_expenses(path):\n    if not path.exists():\n        return 0\n    with path.open(newline="", encoding="utf-8") as f:\n        return sum(int(r["amount"]) for r in csv.DictReader(f))')
para('The functions receive a path, so tests can use temporary files. add_expense writes a header only for a new or empty file. total_expenses returns zero when there is no history yet.',10)

new('21 / Project: make it usable','Part 2: append this below the previous page\'s code')
code('def main():\n    parser = argparse.ArgumentParser(\n        description="A small TZS expense notebook")\n    sub = parser.add_subparsers(dest="command", required=True)\n    add = sub.add_parser("add")\n    add.add_argument("category")\n    add.add_argument("amount", type=int)\n    sub.add_parser("total")\n    args = parser.parse_args()\n    try:\n        if args.command == "add":\n            add_expense(DATA, args.category, args.amount)\n            print("Saved")\n        else:\n            print(f"Total: {total_expenses(DATA)} TZS")\n    except (ValueError, OSError, KeyError, csv.Error) as error:\n        parser.exit(1, f"Cannot complete: {error}\\n")\n\nif __name__ == "__main__":\n    main()')
head('Run it in a fresh project folder')
code('python expenses.py total\npython expenses.py add food 3000\npython expenses.py add travel 1500\npython expenses.py total')
para('Those terminal commands print Total: 0 TZS, Saved, Saved, then Total: 4500 TZS. Running add again appends another record. Keep the generated CSV between sessions to preserve your history.',10)

new('22 / Project: verify & extend','Part 3: save as test_expenses.py beside expenses.py')
code('import tempfile\nimport unittest\nfrom pathlib import Path\nfrom expenses import add_expense, total_expenses\n\nclass ExpenseTests(unittest.TestCase):\n    def test_persistence(self):\n        with tempfile.TemporaryDirectory() as folder:\n            path = Path(folder) / "expenses.csv"\n            self.assertEqual(total_expenses(path), 0)\n            add_expense(path, "food", 3000)\n            add_expense(path, "travel", 1500)\n            self.assertEqual(total_expenses(path), 4500)\n\n    def test_invalid_amount(self):\n        with tempfile.TemporaryDirectory() as folder:\n            path = Path(folder) / "expenses.csv"\n            with self.assertRaises(ValueError):\n                add_expense(path, "food", -1)\n            self.assertFalse(path.exists())')
para('Run python -m unittest -v. Both tests should pass. Then try an empty category and a zero amount manually. Never test destructive file operations against your real data.',10)
head('What this small app does not do yet')
para('It has no dates, editing, currency conversion, simultaneous-writer protection or database transactions. Add a category summary first, then dates, then move storage to SQLite. Malformed existing CSV input is reported as an error, not repaired automatically.',10)

lesson('23 / Automation & office work','Use case: replace a repetitive manual task',
'Python can inventory folders, transform spreadsheets, prepare reports and batch-process documents. Start with a preview that changes nothing. A useful first project is a report of large files or a list of missing documents, followed by a reviewed action.',
'from pathlib import Path\n\nfolder = Path("practice_output")\nfor path in sorted(folder.glob("*.txt")):\n    if path.is_file():\n        print(path.name, path.stat().st_size, "bytes")',
'This prints a file inventory when the practice folder exists; it does not rename or delete anything. For CSV, start with the standard library. Spreadsheet work can use dedicated libraries; preserve formulas and formats when those matter. For scheduled jobs, record what ran, when it ran and whether it succeeded.',
'Build next: generate a CSV inventory with name, size and extension. Check its totals manually on a tiny folder.')
head('Other automation uses')
para('Document generation, email attachment processing, image resizing and business-system integrations share the same pattern: read input, validate it, transform it and produce a traceable result. Decide how repeated runs avoid duplicate outputs.')

lesson('24 / Websites and APIs','Use case: expose data or actions over HTTP / Optional dependency',
'A web backend receives requests and sends responses. An API is a contract for that exchange. FastAPI is one framework for APIs; Django includes a larger web application toolkit, while Flask offers a smaller core. Python usually runs on the server, alongside browser HTML, CSS and JavaScript.',
'# Terminal, inside a virtual environment:\npython -m pip install "fastapi[standard]"\n\n# Save the following Python in main.py:\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("/hello/{name}")\ndef hello(name: str):\n    return {"message": f"Hello, {name}!"}',
'Run fastapi dev main.py in the terminal. Visit http://127.0.0.1:8000/hello/Asha and /docs. The response is JSON with message: Hello, Asha! This development example has no database or authentication. Public deployment needs production configuration, validation, access control and monitoring.',
'Build next: a read-only catalogue API with item IDs, a missing-item response and tests.',ref='https://fastapi.tiangolo.com/tutorial/first-steps/',run=False)

lesson('25 / Data analysis & charts','Use case: turn rows into a useful business question / Optional pandas',
'Analysis starts with a question: which category accounts for the most spending? Check units, missing values and duplicates before calculating. pandas works with labelled tables; charts help communicate the result after the numbers are understood.',
'# Install first: python -m pip install pandas\nimport pandas as pd\n\ndf = pd.DataFrame({\n    "category": ["food", "travel", "food"],\n    "amount": [3000, 1500, 2000],\n})\nsummary = df.groupby("category")["amount"].sum()\nprint(summary)\nprint("Total:", df["amount"].sum())',
'Expected category totals: food = 5000 and travel = 1500; the overall total is 6500. Do not sum unrelated currencies or mix a daily amount with a monthly one. Averages can hide variation: inspect distributions and sample counts too.',
'Build next: a monthly spending report. State the date range, currency, missing rows and the decision the report supports.',ref='https://pandas.pydata.org/docs/getting_started/',run=False)
head('Beyond spreadsheets')
para('Python also powers data pipelines, dashboards and analytics services. Large datasets may need database aggregation or distributed processing; loading everything into one DataFrame is not always appropriate.',10)

new('26 / AI and machine learning','Use case: learn patterns or build applications around trained models')
head('Two different starting points')
para('Traditional machine learning learns a relationship from examples, such as classifying support requests or estimating demand. An application around a language model sends inputs to an existing model and checks its outputs. Neither approach replaces understanding the problem or measuring quality.')
head('A reliable first workflow')
para('Define a target and a simple baseline. Split data into training and evaluation sets before fitting transformations. Train on the training set, evaluate on held-out examples and inspect errors. Choose metrics that match the cost of mistakes; accuracy alone can mislead when classes are imbalanced.')
head('Tools and first project')
para('scikit-learn provides conventional models and evaluation tools. Deep-learning frameworks support larger neural models. Start with a small public labelled dataset and compare a simple baseline with one model. Record the split, features and results so another person can reproduce the experiment.')
head('Language-model applications')
para('A document assistant retrieves relevant passages before drafting an answer. Keep source links, test unsupported questions and verify outputs. Treat retrieved documents as untrusted data. Do not send private data to a service without appropriate permission and controls.')
note('Build next: classify a small set of labelled messages. Write down where the model fails before adding more complexity.')

new('27 / Science & engineering','Use case: calculate, simulate and explain physical or numerical systems')
para('Scientific work often combines arrays, numerical methods and plots. NumPy supports array operations; SciPy provides scientific algorithms. Start with units and assumptions, then compare a computation with a case whose answer you already know.')
code('from math import pi\nfrom statistics import mean, stdev\n\nradius_m = 2\narea_m2 = pi * radius_m ** 2\nreadings = [20.0, 20.2, 19.8, 20.1]\nprint(round(area_m2, 2))\nprint(round(mean(readings), 3))\nprint(round(stdev(readings), 3))')
para('Expected: 12.57, 20.025 and 0.171. stdev calculates sample standard deviation. A precise-looking number is not proof of a precise measurement: sensor uncertainty, calibration and sampling still matter.')
head('Specialist branches')
para('Geospatial work connects records to locations and coordinate systems. Bioinformatics processes biological sequences and experimental results. Finance uses time-series analysis and simulations. Each field needs domain knowledge as well as Python; model assumptions must be reviewed by someone qualified for the application.')
note('Build next: plot a sensor log with units and missing readings clearly identified. Compare the summary against a hand calculation.')

new('28 / Desktop, games & media','Use case: create an interactive or creative tool')
head('Desktop applications')
para('Tkinter offers a route into desktop interfaces; some operating systems require a separate Tk package. A useful first project is a unit converter with two inputs and clear validation. Keep the calculation function independent of the button handler so it can be tested without opening the window.')
head('Games and learning tools')
para('Start with a text quiz, a guessing game or a small 2D game. Learn the loop: receive input, update state, draw the result. Python is useful for learning and prototypes; demanding real-time graphics often rely on engines and lower-level components.')
head('Images, audio and creative workflows')
para('Batch-resize images, generate thumbnails, organise media or script creative software. Keep originals and write outputs into a new folder. Choose output resolution and compression deliberately, then inspect several files rather than assuming a successful command means a good result.')
head('Mobile and browser interfaces')
para('Python can participate in mobile and browser projects, but check the target platform and ecosystem before choosing it for the interface. A common architecture uses a Python API behind a mobile or JavaScript frontend.')
note('Build next: a quiz that records answers and explains mistakes. Add a graphical interface only after the underlying logic works.')

new('29 / Systems, cloud & security','Use case: make software operations observable and repeatable')
head('Operations and cloud automation')
para('Python scripts can inspect logs, check service health, prepare backups and call cloud APIs. Prefer narrowly scoped credentials and explicit resource names. A useful first project reads a log file and counts status codes, without changing any infrastructure.')
head('Testing and quality assurance')
para('Automate API checks, regression tests and browser workflows. Tests should wait for meaningful state rather than arbitrary delays. Keep sample accounts and test data separate from production. Capture enough information to reproduce a failure without logging secrets.')
head('Defensive security')
para('Analyse your own access logs, inventory dependencies and check configuration against a documented baseline. Learn networking and permissions alongside Python. Security automation should operate only on systems you own or have permission to assess.')
head('Hardware and connected devices')
para('Python can coordinate sensors and robotics on suitable computers. MicroPython targets some microcontrollers, but it is not identical to desktop Python; libraries and hardware support differ. Start with reading a sensor and logging a timestamp before controlling motors or physical equipment.')
note('Build next: a log summary that reports the time range, total requests and error count. Verify it on a tiny log you can count by hand.')

new('30 / Pick your next project','Use-case map: problem, first deliverable and what to learn next')
for t,d in [('Automation / Office','A file inventory or CSV report. Learn paths, validation, scheduling and repeatable runs.'),('Web / Business systems','An inventory API. Learn HTTP, SQL, authentication, authorisation and deployment.'),('Data / Dashboards','A spending analysis. Learn pandas, statistics, plotting and data-quality checks.'),('AI / Language / Vision','A labelled-data experiment. Learn evaluation, leakage prevention and error analysis.'),('Science / GIS / Research','A reproducible analysis notebook. Learn units, numerical methods and domain assumptions.'),('Desktop / Games / Media','A converter, quiz or image pipeline. Learn event-driven code and user feedback.'),('Cloud / Testing / Security','A health or log report. Learn APIs, permissions, testing and observability.'),('IoT / Education','A sensor logger or teaching exercise. Learn hardware constraints and clear feedback.')]:
    head(t);para(d,10,gap=5)

new('31 / Work like a professional','Make it understandable, reproducible and safe to change')
head('A small project structure')
code('my_project/\n  README.md\n  pyproject.toml\n  src/\n    my_app/\n      __init__.py\n      core.py\n  tests/\n    test_core.py\n  .gitignore')
para('Start simple; adopt this layout when packaging helps. Write a README with setup, run commands, expected input and tests. Record a supported Python version. A dependency record or lockfile should capture the environment that you actually tested.')
head('Before a release')
para('Run tests from a clean environment. Check invalid input and empty data. Keep secrets out of source control. Log useful events without passwords or personal data. Back up persistent data and verify restoration. Write an update note describing what changed.')
head('When it becomes slow')
para('Measure first. Improve the algorithm or reduce unnecessary I/O before adding concurrency. async helps coordinate waiting tasks; it does not automatically accelerate CPU-heavy calculations. Use processes or specialised numeric tools when measurements justify them.')
note('A project is ready to share when another person can set it up, understand its limits and reproduce its result.')

new('32 / Practice and answers','Try first. Cover the answer before reading it.')
head('A / Sum selected values')
para('Task: total only amounts above 1000 from [500, 1500, 2000]. Expected: 3500.',10)
code('amounts = [500, 1500, 2000]\nanswer = sum(x for x in amounts if x > 1000)\nprint(answer)')
head('B / Count words')
para('Task: count the words in "code learn code". Expected: code appears twice and learn once.',10)
code('counts = {}\nfor word in "code learn code".split():\n    counts[word] = counts.get(word, 0) + 1\nprint(counts)')
head('C / Fix the shared-list surprise')
para('Task: a = [1]; b = a; b.append(2). Why is a now [1, 2]? Both names refer to the same list. Use b = a.copy() for an independent shallow copy.',10)
head('D / Project acceptance checks')
para('A fresh total is zero. Two entries of 3000 and 1500 total 4500. A negative amount does not create a file. Empty categories are rejected. Running total twice leaves the stored data unchanged.',10)

new('33 / Your four-week route','A suggested pace; move on when you can explain what you built')
for t,d in [('Week 1 / Read and change code','Pages 3-12. Practise 30-45 minutes a day. Build a price calculator and a short quiz. Explain each variable and branch without looking at the example.'),('Week 2 / Organise and save','Pages 13-21. Split calculations into functions. Read and write CSV. Add tests. Build a contact list using fictional data.'),('Week 3 / Finish one project','Pages 22-24. Run the expense notebook, test it and add a category summary. Write a README and save changes in Git.'),('Week 4 / Choose one direction','Pages 25-32. Pick automation, web, data or another field. Deliver a small working version with sample input, expected output and documented limitations.')]:
    head(t);para(d)
head('When you get stuck')
para('Read the error carefully. Reduce the problem to a few lines. Print the values you assumed were correct. Check the relevant documentation. Ask a precise question that includes the code, expected result and actual result.')
note('Progress is a small project you can explain and improve, not the number of libraries you have installed.')

new('34 / Reference shelf','Official documentation and a short glossary')
refs=[('Python tutorial and language reference','https://docs.python.org/3/tutorial/'),('Standard library: files, CSV, JSON, tests, SQL','https://docs.python.org/3/library/'),('Install Python','https://www.python.org/downloads/'),('Environments and packages','https://packaging.python.org/en/latest/tutorials/installing-packages/'),('Application areas','https://www.python.org/about/apps/'),('FastAPI: first steps','https://fastapi.tiangolo.com/tutorial/first-steps/'),('pandas: getting started','https://pandas.pydata.org/docs/getting_started/'),('Machine learning: scikit-learn','https://scikit-learn.org/stable/getting_started.html')]
for label,url in refs:
    start=y;para(label,14,'Hand',gap=0);para(url,7.3,gap=7);c.linkURL(url,(82,y,544,start),relative=0)
head('Words to remember')
para('Interpreter: runs Python code. Iterable: supplies successive values. Function: reusable operation. Module: importable code. Exception: a reported failure. API: an interface contract. Dependency: software your project requires. Test: an executable check of expected behaviour.',9,gap=8)
para('Documentation reviewed 19 October 2026. Core lessons use stable Python 3 features. Optional ecosystem examples may require updated dependencies; consult their official compatibility guidance.',8.5)
c.save()
(ROOT/'studio/python-notebook/lesson.md').write_text('\n'.join(plain))
import json
(ROOT/'studio/python-notebook/examples.json').write_text(json.dumps(examples,indent=2))
print(f'{OUT}\n{page} pages')
