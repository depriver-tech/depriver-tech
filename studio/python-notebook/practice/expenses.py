import argparse
import csv
from pathlib import Path

DATA = Path(__file__).resolve().with_name("expenses.csv")

def add_expense(path, category, amount):
    category = category.strip()
    if not category or amount <= 0:
        raise ValueError("Category and positive amount required")
    new_file = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["category", "amount"])
        writer.writerow([category, amount])

def total_expenses(path):
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8") as f:
        return sum(int(r["amount"]) for r in csv.DictReader(f))

def main():
    parser = argparse.ArgumentParser(
        description="A small TZS expense notebook")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("category")
    add.add_argument("amount", type=int)
    sub.add_parser("total")
    args = parser.parse_args()
    try:
        if args.command == "add":
            add_expense(DATA, args.category, args.amount)
            print("Saved")
        else:
            print(f"Total: {total_expenses(DATA)} TZS")
    except (ValueError, OSError, KeyError, csv.Error) as error:
        parser.exit(1, f"Cannot complete: {error}\n")

if __name__ == "__main__":
    main()
