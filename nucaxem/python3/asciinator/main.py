# autoren: joel ganser (peogrammierung) jann luebben (rum sitzen und porn guckwn)
import json

print("=" * 30)
print("v.0.3")
print("ASCIINATOR")
print("made by joel ganser 2025 (c) ")
print("your ASCII Art generator!")
print("=" * 30)




with open("db.json", "r", encoding="utf-8") as f:
    db = json.load(f)

char = input("enter your letter: ").strip()

print("\your input was :", char)
print(.)

found = False






for key, art in db.items():
    if char in key.split(","):
        for line in art:
            print(line)
        found = True
        break

if not found:
    print("no fucking database w data base lol add more things pls :sob:")
    print("or add database cause no farking fallback i am to soby to so ts  rose emoji")
