# 10 / Functions that return
def line_total(price: int, quantity: int = 1) -> int:
    if price < 0 or quantity < 0:
        raise ValueError("Use non-negative values")
    return price * quantity

first = line_total(1500, 3)
second = line_total(price=500)
print(first + second)
