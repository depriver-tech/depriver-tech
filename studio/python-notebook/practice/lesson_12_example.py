# 13 / Errors are information
raw = "not a number"
try:
    quantity = int(raw)
except ValueError:
    print("Enter a whole number")
else:
    print(quantity * 1500)
finally:
    print("Check complete")
