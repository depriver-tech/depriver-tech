# 15 / CSV and JSON
import csv
import io
import json

source = "category,amount\nfood,3000\ntravel,1500\n"
rows = list(csv.DictReader(io.StringIO(source)))
total = sum(int(row["amount"]) for row in rows)
report = {"currency": "TZS", "total": total}
encoded = json.dumps(report, indent=2)
print(encoded)
print(json.loads(encoded)["total"])
