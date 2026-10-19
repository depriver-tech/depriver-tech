# 12 / Modules and packages
from statistics import mean
from datetime import date

scores = [60, 75, 90]
print(mean(scores))
print(date(2026, 10, 19).isoformat())

def main():
    print("Notebook ready")

if __name__ == "__main__":
    main()
