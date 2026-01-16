# coded by Jann Lübben and Joel Ganser
import json # uses json library because the ascii letters are stored in a json file

print("=" * 30) # prints 30 "="
print("v.0.5") # version
print("ASCIINATOR") # name of the tool
print("made by joel ganser and Jann Lübben") # credits
print("your ASCII Art generator!")
print("=" * 30) # again prints 30 "="

with open("db.json", "r", encoding="utf-8") as f: # conf the load
    db = json.load(f) # load the .json

while True: #infinite loop
    # working because it does not need anything after loading the db
    char = input("\nenter your letter (or exit): ").strip() # asks for input (letter and also exit)

    if char.lower() == "exit": # exit
        break # closes

    print("your input was:", char)
    found = False # get found false

    for key, art in db.items():
        if char in key.split(","):
            for line in art:
                print(line)
            found = True
            break

    if not found:
        print("versuch etwas anderes") # get the user to try something different
