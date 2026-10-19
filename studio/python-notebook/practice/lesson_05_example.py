# 06 / Make decisions
budget = 5000
cost = 4200
if cost < 0:
    print("Invalid cost")
elif cost <= budget:
    print("Within budget")
else:
    print("Over budget")

is_member = True
print(is_member and cost <= budget)
