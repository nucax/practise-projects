import time
import json
import threading
from tkinter import *
from tkinter import ttk, simpledialog
from pynput import keyboard, mouse

SAVE_FILE = "macros.json"
MAX_MACROS = 10

class MacroManager:
    def __init__(self):
        self.macros = [
            {"name": f"Macro {i+1}", "hotkey": None, "actions": []}
            for i in range(MAX_MACROS)
        ]
        self.recording_index = None
        self.start_time = None
        self.recording = False

        self.load()

    # ---------- SAVE / LOAD ----------
    def save(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.macros, f, default=str)

    def load(self):
        try:
            with open(SAVE_FILE, "r") as f:
                self.macros = json.load(f)
        except:
            pass

    # ---------- RECORD ----------
    def start_recording(self, index):
        self.recording_index = index
        self.macros[index]["actions"] = []
        self.start_time = time.time()
        self.recording = True
        status.set(f"Recording {self.macros[index]['name']}")

    def stop_recording(self):
        self.recording = False
        self.save()
        status.set("Stopped")

    def record(self, action_type, data):
        if self.recording:
            t = time.time() - self.start_time
            self.macros[self.recording_index]["actions"].append((t, action_type, data))

    # ---------- PLAY ----------
    def play(self, index):
        actions = self.macros[index]["actions"]
        if not actions:
            status.set("No actions")
            return

        status.set(f"Playing {self.macros[index]['name']}")
        k = keyboard.Controller()
        m = mouse.Controller()
        start = time.time()

        for t, action, data in actions:
            while time.time() - start < t:
                time.sleep(0.001)

            if action == "kp": k.press(data)
            elif action == "kr": k.release(data)
            elif action == "mc":
                x, y, b, p = data
                m.position = (x, y)
                m.press(b) if p else m.release(b)
            elif action == "mm": m.position = data
            elif action == "ms":
                x, y, dx, dy = data
                m.position = (x, y)
                m.scroll(dx, dy)

        status.set("Done")

manager = MacroManager()

# ---------- GLOBAL LISTENERS ----------
def input_listener():
    def on_press(key):
        if manager.recording:
            manager.record("kp", key)

        for i, mdata in enumerate(manager.macros):
            if mdata["hotkey"] and str(key) == mdata["hotkey"]:
                threading.Thread(target=manager.play, args=(i,), daemon=True).start()

    def on_release(key):
        if manager.recording:
            manager.record("kr", key)

    def on_click(x, y, button, pressed):
        manager.record("mc", (x, y, button, pressed))

    def on_move(x, y):
        manager.record("mm", (x, y))

    def on_scroll(x, y, dx, dy):
        manager.record("ms", (x, y, dx, dy))

    keyboard.Listener(on_press=on_press, on_release=on_release).start()
    mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll).start()

threading.Thread(target=input_listener, daemon=True).start()

# ---------- UI ----------
root = Tk()
root.title("Macro Manager")

status = StringVar(value="Idle")
Label(root, textvariable=status).pack(pady=5)

frame = ttk.Frame(root)
frame.pack(fill=BOTH, expand=True)

tree = ttk.Treeview(frame, columns=("Hotkey"), show="headings", height=10)
tree.heading("Hotkey", text="Hotkey")
tree.pack(fill=BOTH, expand=True)

def refresh():
    tree.delete(*tree.get_children())
    for i, m in enumerate(manager.macros):
        tree.insert("", END, iid=i, values=(f"{m['name']}  ({m['hotkey']})",))

refresh()

# ---------- ACTIONS ----------
def record_macro():
    sel = tree.selection()
    if not sel: return
    i = int(sel[0])
    manager.start_recording(i)

def stop_record():
    manager.stop_recording()
    refresh()

def play_macro(event=None):
    sel = tree.selection()
    if not sel: return
    i = int(sel[0])
    threading.Thread(target=manager.play, args=(i,), daemon=True).start()

def rename_macro():
    sel = tree.selection()
    if not sel: return
    i = int(sel[0])
    name = simpledialog.askstring("Rename", "Macro name:")
    if name:
        manager.macros[i]["name"] = name
        manager.save()
        refresh()

def set_hotkey():
    sel = tree.selection()
    if not sel: return
    i = int(sel[0])
    key = simpledialog.askstring("Hotkey", "Enter key (example: Key.f6):")
    if key:
        manager.macros[i]["hotkey"] = key
        manager.save()
        refresh()

btns = Frame(root)
btns.pack(pady=5)

Button(btns, text="Record", command=record_macro).grid(row=0, column=0, padx=5)
Button(btns, text="Stop", command=stop_record).grid(row=0, column=1, padx=5)
Button(btns, text="Rename", command=rename_macro).grid(row=0, column=2, padx=5)
Button(btns, text="Set Hotkey", command=set_hotkey).grid(row=0, column=3, padx=5)

tree.bind("<Double-1>", play_macro)

root.mainloop()
