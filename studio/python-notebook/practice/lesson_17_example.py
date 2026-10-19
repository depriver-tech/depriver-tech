# 18 / A small database
import sqlite3

con = sqlite3.connect(":memory:")
try:
    con.execute("CREATE TABLE expenses "
                "(category TEXT, amount INTEGER)")
    con.execute("INSERT INTO expenses VALUES (?, ?)",
                ("food", 3000))
    con.commit()
    row = con.execute(
        "SELECT SUM(amount) FROM expenses"
    ).fetchone()
    print(row[0])
finally:
    con.close()
