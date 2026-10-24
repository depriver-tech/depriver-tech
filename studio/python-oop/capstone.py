"""In-memory teaching model; run with python capstone.py."""
from dataclasses import dataclass


def required_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty text")
    return value.strip()


@dataclass(frozen=True)
class Book:
    code: str
    title: str

    def __post_init__(self):
        object.__setattr__(self, "code", required_text(self.code, "code"))
        object.__setattr__(self, "title", required_text(self.title, "title"))


class LoanError(Exception):
    """A valid book cannot undergo the requested loan transition."""


class Library:
    def __init__(self):
        self._books = {}
        self._loans = {}

    def __len__(self):
        return len(self._books)

    def add(self, book):
        if not isinstance(book, Book):
            raise TypeError("Book required")
        if book.code in self._books:
            raise ValueError("duplicate book code")
        self._books[book.code] = book

    def get(self, code):
        return self._books[code]

    def lend(self, code, borrower):
        self.get(code)  # KeyError identifies an unknown physical copy.
        borrower = required_text(borrower, "borrower")
        if code in self._loans:
            raise LoanError("copy already on loan")
        self._loans[code] = borrower

    def return_book(self, code):
        self.get(code)
        if code not in self._loans:
            raise LoanError("copy is not on loan")
        return self._loans.pop(code)

    def available(self, code):
        self.get(code)
        return code not in self._loans

    def active_loans(self):
        # A snapshot avoids exposing our mutable internal mapping.
        return dict(self._loans)


def main():
    library = Library()
    library.add(Book("P1", "Python"))
    library.add(Book("G1", "Git"))
    library.lend("P1", "Asha")
    print("Active loans:", library.active_loans())
    print("Returned by:", library.return_book("P1"))
    print("Python available:", library.available("P1"))


if __name__ == "__main__":
    main()
