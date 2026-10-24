import unittest
from dataclasses import FrozenInstanceError
from capstone import Book, Library, LoanError


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.library.add(Book("P1", "Python"))

    def test_new_copy_available(self):
        self.assertEqual(len(self.library), 1)
        self.assertTrue(self.library.available("P1"))

    def test_lend_then_return(self):
        self.library.lend("P1", "Asha")
        self.assertFalse(self.library.available("P1"))
        self.assertEqual(self.library.return_book("P1"), "Asha")
        self.assertTrue(self.library.available("P1"))

    def test_duplicate_loan_preserves_borrower(self):
        self.library.lend("P1", "Asha")
        with self.assertRaises(LoanError):
            self.library.lend("P1", "Juma")
        self.assertEqual(self.library.active_loans(), {"P1": "Asha"})

    def test_return_without_loan(self):
        with self.assertRaises(LoanError):
            self.library.return_book("P1")
        self.assertTrue(self.library.available("P1"))

    def test_unknown_copy_operations(self):
        for operation in (lambda: self.library.get("X"),
                          lambda: self.library.lend("X", "Asha"),
                          lambda: self.library.return_book("X"),
                          lambda: self.library.available("X")):
            with self.subTest(operation=operation):
                with self.assertRaises(KeyError):
                    operation()
        self.assertEqual(self.library.active_loans(), {})

    def test_duplicate_code_preserves_original(self):
        with self.assertRaises(ValueError):
            self.library.add(Book("P1", "Replacement"))
        self.assertEqual(self.library.get("P1").title, "Python")
        self.assertEqual(len(self.library), 1)

    def test_blank_or_wrong_borrower_rejected(self):
        for borrower in ("", "  ", None, 3):
            with self.subTest(borrower=borrower):
                with self.assertRaises(ValueError):
                    self.library.lend("P1", borrower)
                self.assertTrue(self.library.available("P1"))

    def test_invalid_records_rejected(self):
        for code, title in (("", "Python"), ("P1", " "), (None, "Git"), ("P1", 5)):
            with self.subTest(code=code, title=title):
                with self.assertRaises(ValueError):
                    Book(code, title)

    def test_normalises_text(self):
        self.assertEqual(Book(" P2 ", " Git "), Book("P2", "Git"))
        self.library.lend("P1", " Asha ")
        self.assertEqual(self.library.active_loans(), {"P1": "Asha"})

    def test_snapshot_does_not_expose_internal_state(self):
        self.library.lend("P1", "Asha")
        snapshot = self.library.active_loans()
        snapshot.clear()
        self.assertEqual(self.library.active_loans(), {"P1": "Asha"})

    def test_libraries_are_independent(self):
        other = Library()
        self.assertEqual(len(other), 0)
        self.library.lend("P1", "Asha")
        self.assertEqual(other.active_loans(), {})

    def test_book_is_frozen_and_hashable(self):
        book = Book("P1", "Python")
        with self.assertRaises(FrozenInstanceError):
            book.code = "P2"
        self.assertEqual(len({book, Book("P1", "Python")}), 1)

    def test_multiple_copies_same_title(self):
        self.library.add(Book("P2", "Python"))
        self.library.lend("P1", "Asha")
        self.assertTrue(self.library.available("P2"))

    def test_wrong_record_type(self):
        with self.assertRaises(TypeError):
            self.library.add({"code": "P2"})

    def test_repeated_return_rejected(self):
        self.library.lend("P1", "Asha")
        self.library.return_book("P1")
        with self.assertRaises(LoanError):
            self.library.return_book("P1")

    def test_returned_copy_can_be_lent_again(self):
        self.library.lend("P1", "Asha")
        self.library.return_book("P1")
        self.library.lend("P1", "Juma")
        self.assertEqual(self.library.active_loans(), {"P1": "Juma"})


if __name__ == "__main__":
    unittest.main()
