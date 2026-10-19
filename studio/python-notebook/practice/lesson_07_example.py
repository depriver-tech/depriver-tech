# 08 / Dictionaries and sets
student = {"name": "Asha", "score": 82}
student["city"] = "Mbeya"
print(student["name"])
print(student.get("phone", "Not supplied"))
for key, value in student.items():
    print(key, value)

skills = {"Python", "SQL", "Python"}
print(len(skills))
print("SQL" in skills)
