import os
import json
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

# Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CUSTOM_GAMES_DIR = os.path.join(SCRIPT_DIR, "Games")
STEAM_ROOT = os.path.expanduser("~/.steam/steam")
STEAM_APPS = os.path.join(STEAM_ROOT, "steamapps")
COMPATDATA = os.path.join(STEAM_APPS, "compatdata")

def parse_acf(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        appid, name, installdir = None, None, None
        for line in lines:
            if '"appid"' in line:
                appid = line.split('"')[3]
            elif '"name"' in line:
                name = line.split('"')[3]
            elif '"installdir"' in line:
                installdir = line.split('"')[3]
            if appid and name and installdir:
                return {"appid": appid, "name": name, "installdir": installdir}
    except Exception as e:
        print(f"Error parsing {path}: {e}")
    return None

def find_exe_in(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".exe"):
                return os.path.join(root, file)
    return None

def get_steam_games():
    games = []
    if not os.path.exists(STEAM_APPS):
        return games
    for fname in os.listdir(STEAM_APPS):
        if fname.startswith("appmanifest") and fname.endswith(".acf"):
            game = parse_acf(os.path.join(STEAM_APPS, fname))
            if game:
                appid = game["appid"]
                name = game["name"]
                pfx_path = os.path.join(COMPATDATA, appid, "pfx", "drive_c")
                if os.path.exists(pfx_path):
                    exe_path = find_exe_in(pfx_path)
                    if exe_path:
                        games.append({"name": f"[Steam] {name}", "path": exe_path})
    return games

def get_local_games():
    games = []
    if not os.path.exists(CUSTOM_GAMES_DIR):
        os.makedirs(CUSTOM_GAMES_DIR)
    for fname in os.listdir(CUSTOM_GAMES_DIR):
        if fname.lower().endswith(".exe"):
            full_path = os.path.join(CUSTOM_GAMES_DIR, fname)
            games.append({"name": fname, "path": full_path})
    return games

def launch_game(path):
    if path is None:
        root.quit()
    elif os.path.exists(path):
        subprocess.Popen(["wine", path])
    else:
        messagebox.showerror("Error", f"File not found:\n{path}")

# Build game list
games = get_steam_games() + get_local_games()
games.append({"name": "Quit", "path": None})

# GUI setup
root = tk.Tk()
root.title("Game Launcher")
root.geometry("450x500")
root.configure(bg="#1e1e1e")

title = tk.Label(root, text="Game Launcher", font=("Helvetica", 18, "bold"), bg="#1e1e1e", fg="white")
title.pack(pady=10)

# Scrollable frame
frame_container = tk.Frame(root)
canvas = tk.Canvas(frame_container, bg="#1e1e1e", highlightthickness=0)
scrollbar = ttk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

frame_container.pack(fill="both", expand=True, padx=10, pady=10)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Game buttons
for game in games:
    name = game["name"]
    path = game["path"]
    btn = tk.Button(scrollable_frame, text=name, width=50, height=2,
                    command=lambda p=path: launch_game(p),
                    bg="#2e2e2e", fg="white", activebackground="#3e3e3e", bd=0, font=("Helvetica", 10, "bold"))
    btn.pack(pady=5)

root.mainloop()

