# 16 / Classes and dataclasses
from dataclasses import dataclass

@dataclass
class Expense:
    category: str
    amount: int

    def label(self):
        return f"{self.category}: {self.amount} TZS"

entry = Expense("food", 3000)
print(entry.label())
