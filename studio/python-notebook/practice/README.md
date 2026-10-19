# Python: the practical notebook - practice files
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
