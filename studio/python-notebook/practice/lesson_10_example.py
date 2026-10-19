# 11 / Comprehensions & generators
prices = [100, 200, 300, 400]
large = [p for p in prices if p >= 300]
print(large)

def squares(limit):
    for n in range(limit):
        yield n * n

values = squares(4)
print(list(values))
print(list(values))
