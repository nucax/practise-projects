import os, sys, subprocess

desktop = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop, "correct.txt")

with open(file_path, "w") as f:
    f.write("Good.")

if os.name == "nt":
    os.startfile(file_path)
elif os.name == "posix":
    subprocess.call(["open" if sys.platform == "darwin" else "xdg-open", file_path])
