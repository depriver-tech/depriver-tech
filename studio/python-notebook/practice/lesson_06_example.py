# 07 / Lists and tuples
items = ["pen", "book"]
items.append("bag")
print(items[0], items[-1])
print(items[:2])
print(len(items))
copy = items.copy()
copy.append("ruler")
print(len(items), len(copy))
location = (-8.9, 33.4)
latitude, longitude = location
