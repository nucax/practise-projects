import json

print("=" * 30)
print("v.0.4")
print("ASCIINATOR")
print("made by joel ganser and Jann Lübben")
print("your ASCII Art generator!")
print("=" * 30)




with open("db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

char = input("enter your letter: ").strip()
print("your input was :", char)

found = False






for key, art in db.items():
    if char in key.split(","):
        for line in art:
            print(line)
        found = True
        break

if not found:
    print("versuch etwas anderes")
