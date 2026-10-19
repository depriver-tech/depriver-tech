# 09 / Repeat with loops
prices = [1000, 2500, 500]
for number, price in enumerate(prices, start=1):
    print(number, price)

remaining = 3
while remaining > 0:
    print("Attempts:", remaining)
    remaining -= 1

print(sum(prices))
