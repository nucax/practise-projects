import json

print("=" * 30)
print("v.0.3")
print("ASCIINATOR")
print("your ASCII Art generator!")
print("=" * 30)




with open("db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

char = input("enter your letter: ").strip()

print("\your input:", char)
print()

found = False






for key, art in db.items():
    if char in key.split(","):
        for line in art:
            print(line)
        found = True
        break

if not found:
    print("no fucking database w data base lol add more things pls :sob:")
