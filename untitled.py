import tkinter as tk
from tkinter import messagebox
import random
import time
import math

# optionally use pygame for music/sfx; fallback if unavailable
try:
    import pygame
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False

MUSIC_FILE = "fun.mp3"  # put your music file here

if AUDIO_AVAILABLE:
    try:
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(loops=-1)
    except Exception:
        # music fails silently if file missing
        pass

# ---------- Warning and Main Menu ----------

def show_warning(parent=None):
    warning_message = (
        "WARNING\n\n"
        "This game is intended for players 18 years or older.\n"
        "It contains graphic content including blood, gore, death, self-harm, suicide, and drug use.\n"
        "If you are struggling with mental health, playing this game may make it worse.\n"
        "Player discretion is strongly advised."
    )
    messagebox.showwarning("warning..", warning_message)
    open_main_menu()

def open_main_menu():
    # create the main window (fullscreen)
    main_root = tk.Tk()
    main_root.title("Untitled Game")
    main_root.configure(bg="black")
    main_root.attributes("-fullscreen", True)

    # stop music & close
    def on_exit():
        if AUDIO_AVAILABLE:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        main_root.destroy()

    # layout frames
    menu_frame = tk.Frame(main_root, bg="black")
    ascii_frame = tk.Frame(main_root, bg="black")

    ascii_art = '''
       .-""""-.
     .'        '.
    /            \\
   |,  .-.  .-.  ,|
   | )(_o/  \\o_)( |
   |/     /\\     \\|
   (_     ^^     _)
    \\__|IIIIII|__/
     | \\IIIIII/ |
     \\          /
      `--------`
    '''
    ascii_label = tk.Label(ascii_frame, text=ascii_art, fg="white", bg="black", justify="left")
    ascii_label.pack(expand=True)

    title_label = tk.Label(menu_frame, text="UNTITLED GAME :(", fg="grey", bg="black", anchor="w")
    title_label.pack(pady=(0, 50), anchor="w")

    # Start Game opens a Toplevel game window (so menu stays alive)
    def start_game():
        # disable start button (prevent multiple windows)
        start_btn.config(state="disabled")
        GameWindow(main_root, on_game_close=lambda: start_btn.config(state="normal"))

    start_btn = tk.Button(menu_frame, text="Start Game", bg="grey", fg="black", command=start_game)
    start_btn.pack(pady=10, anchor="w")

    exit_btn = tk.Button(menu_frame, text="Exit", bg="grey", fg="black", command=on_exit)
    exit_btn.pack(pady=10, anchor="w")

    buttons = [start_btn, exit_btn]

    def update_layout(event=None):
        width = main_root.winfo_width()
        height = main_root.winfo_height()
        # use relative placement for more consistent fullscreen layout
        menu_frame.place(relx=0.05, rely=0.08, relwidth=0.38, relheight=0.84)
        ascii_frame.place(relx=0.45, rely=0.08, relwidth=0.5, relheight=0.84)
        title_label.config(font=("Courier", max(16, int(height * 0.07))))
        for btn in buttons:
            btn.config(font=("Arial", max(10, int(height * 0.03))))
        ascii_label.config(font=("Courier", max(8, int(height * 0.02))))

    main_root.bind("<Configure>", update_layout)
    # ESC to exit the menu + stop music
    main_root.bind("<Escape>", lambda e: on_exit())
    update_layout()
    main_root.mainloop()

# ---------- Game Window & Logic ----------

class GameWindow:
    def __init__(self, parent, on_game_close=None):
        self.parent = parent
        self.on_game_close = on_game_close
        self.win = tk.Toplevel(parent)
        self.win.title("Endless Survival")
        self.win.configure(bg="black")
        self.win.attributes("-fullscreen", True)

        # canvas for rendering
        self.canvas = tk.Canvas(self.win, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # sizes and scaling
        self.width = self.win.winfo_screenwidth()
        self.height = self.win.winfo_screenheight()

        # game state
        self.running = True
        self.paused = False
        self.start_time = time.time()
        self.last_tick = time.time()
        self.score = 0.0

        self.health = 100.0
        self.max_health = 100.0
        self.health_drain_rate = 0.02  # per tick (approx per 20 ms)
        self.hallucination_intensity = 0  # extra spawn factor
        self.hallucination_end_time = 0

        # player
        self.player_size = 18
        self.player_x = self.width // 2
        self.player_y = self.height // 2
        self.player_speed = 6

        # drugs inventory
        self.drugs = 0
        self.drug_heal = 35
        self.drug_cooldown = 1.2  # seconds between uses
        self.drug_last_used = -999

        # pickups and enemies
        self.pills = []  # list of (id, x, y)
        self.hallucinations = []  # list of dicts: {'id','x','y','vx','vy','hp','flicker'}
        self.spawn_counter = 0
        self.spawn_base_interval = 2.2  # seconds
        self.last_spawn = time.time()

        # UI items (text)
        self.health_text = self.canvas.create_text(20, 20, anchor="nw", fill="white", font=("Arial", 14), text="")
        self.drug_text = self.canvas.create_text(20, 44, anchor="nw", fill="white", font=("Arial", 12), text="")
        self.score_text = self.canvas.create_text(20, 64, anchor="nw", fill="white", font=("Arial", 12), text="")
        self.hint_text = self.canvas.create_text(self.width - 20, 20, anchor="ne", fill="grey", font=("Arial", 12),
                                                 text="Move: arrows/WASD   Use Drug: D   Pause: P   Exit: ESC")

        # bind keys
        self.keys = set()
        self.win.bind("<KeyPress>", self.on_key_down)
        self.win.bind("<KeyRelease>", self.on_key_up)
        self.win.bind("<Escape>", lambda e: self.end_game())
        self.win.bind("<FocusOut>", lambda e: self.pause_game(True))

        # initial objects
        self.player_obj = None
        self.draw_player()
        for _ in range(3):
            self.spawn_pill()

        # start loop
        self.tick()

    # key handlers
    def on_key_down(self, event):
        key = event.keysym.lower()
        self.keys.add(key)
        if key == "p":
            self.pause_game(not self.paused)
        if key == "d":
            self.use_drug()

    def on_key_up(self, event):
        key = event.keysym.lower()
        if key in self.keys:
            self.keys.remove(key)

    def pause_game(self, state=None):
        if state is None:
            state = not self.paused
        self.paused = state
        if self.paused:
            self.canvas.itemconfigure(self.hint_text, text="PAUSED - Press P to resume")
        else:
            self.canvas.itemconfigure(self.hint_text, text="Move: arrows/WASD   Use Drug: D   Pause: P   Exit: ESC")
            # continue ticking
            self.last_tick = time.time()

    # drawing
    def draw_player(self):
        if self.player_obj:
            self.canvas.delete(self.player_obj)
        x, y, r = self.player_x, self.player_y, self.player_size
        self.player_obj = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", outline="grey")

    def spawn_pill(self):
        # spawn a pill somewhere not too close to player
        margin = 80
        while True:
            x = random.randint(margin, self.width - margin)
            y = random.randint(margin, self.height - margin)
            if math.hypot(x - self.player_x, y - self.player_y) > 120:
                break
        pill_id = self.canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill="purple", outline="white")
        self.pills.append((pill_id, x, y))

    def spawn_hallucination(self):
        # spawn enemy at random edge, heading towards player
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x = random.randint(0, self.width)
            y = -30
        elif side == "bottom":
            x = random.randint(0, self.width)
            y = self.height + 30
        elif side == "left":
            x = -30
            y = random.randint(0, self.height)
        else:
            x = self.width + 30
            y = random.randint(0, self.height)

        angle = math.atan2(self.player_y - y, self.player_x - x)
        base_speed = 1.0 + 0.03 * (time.time() - self.start_time)  # slowly ramp up
        intensity_bonus = 0.6 * self.hallucination_intensity
        speed = base_speed + intensity_bonus + random.uniform(0, 0.6)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        hp = 6 + int(self.hallucination_intensity * 1.5)
        color = "#8B0000"  # dark red
        item = self.canvas.create_oval(x - 12, y - 12, x + 12, y + 12, fill=color, outline="")
        h = {'id': item, 'x': x, 'y': y, 'vx': vx, 'vy': vy, 'hp': hp, 'flicker': random.random() * 0.3}
        self.hallucinations.append(h)

    # using drugs
    def use_drug(self):
        now = time.time()
        if now - self.drug_last_used < self.drug_cooldown:
            return
        if self.drugs <= 0:
            return
        self.drugs -= 1
        self.drug_last_used = now
        # heal
        self.health = min(self.max_health, self.health + self.drug_heal)
        # intensify hallucinations for a short time
        self.hallucination_intensity += 2
        self.hallucination_end_time = now + 10.0  # intensity lasts 10s
        # visual/SFX cue - optional pygame sound
        if AUDIO_AVAILABLE:
            try:
                # try play a short tone if provided as "drug.wav"
                s = pygame.mixer.Sound("drug.wav")
                s.play()
            except Exception:
                pass

    # collision helpers
    def collide_player_with_pills(self):
        new_pills = []
        for pid, x, y in self.pills:
            if math.hypot(x - self.player_x, y - self.player_y) < self.player_size + 10:
                # pick up
                self.canvas.delete(pid)
                self.drugs += 1
                # respawn a pill later
                self.win.after(5000, self.spawn_pill)
            else:
                new_pills.append((pid, x, y))
        self.pills = new_pills

    def collide_player_with_hallucinations(self):
        # hallucinations damage player on contact
        remaining = []
        for h in self.hallucinations:
            d = math.hypot(h['x'] - self.player_x, h['y'] - self.player_y)
            if d < self.player_size + 12:
                # damage
                self.health -= 0.28  # per tick while touching
                # slight recoil: push hallucination away
                if d == 0:
                    d = 0.1
                nx = (h['x'] - self.player_x) / d
                ny = (h['y'] - self.player_y) / d
                h['x'] += nx * 8
                h['y'] += ny * 8
                # they lose some hp (the player fights with reality)
                h['hp'] -= 0.7
            if h['hp'] > 0 and -200 < h['x'] < self.width + 200 and -200 < h['y'] < self.height + 200:
                remaining.append(h)
            else:
                # remove from canvas
                try:
                    self.canvas.delete(h['id'])
                except Exception:
                    pass
        self.hallucinations = remaining

    # update and render loop
    def tick(self):
        if not self.running:
            return
        now = time.time()
        dt = now - self.last_tick
        self.last_tick = now
        if not self.paused:
            # time survived
            self.score = now - self.start_time

            # health passive drain
            self.health -= self.health_drain_rate * (dt * 50.0)  # scale drain to feel right

            # move player based on keys
            dx = dy = 0
            if any(k in self.keys for k in ("left", "a")):
                dx -= self.player_speed
            if any(k in self.keys for k in ("right", "d")) and False:
                # careful: 'd' is also drug key - prefer arrow keys for right movement
                dx += self.player_speed
            if any(k in self.keys for k in ("right", "d", "l")):
                # allow right arrow and l as alternative
                if "d" not in self.keys:  # if pressing 'd' to use drug, keep moving allowed
                    pass
                dx += self.player_speed
            if any(k in self.keys for k in ("up", "w")):
                dy -= self.player_speed
            if any(k in self.keys for k in ("down", "s")):
                dy += self.player_speed
            # normalize diagonal
            if dx != 0 and dy != 0:
                dx *= 0.7071
                dy *= 0.7071
            self.player_x = max(20, min(self.width - 20, self.player_x + dx))
            self.player_y = max(20, min(self.height - 20, self.player_y + dy))
            self.draw_player()

            # update hallucination intensity decay
            if time.time() > self.hallucination_end_time:
                # slowly reduce intensity
                if self.hallucination_intensity > 0:
                    self.hallucination_intensity = max(0, self.hallucination_intensity - 0.02)

            # spawn logic
            spawn_wait = max(0.5, self.spawn_base_interval - 0.06 * (time.time() - self.start_time) - 0.12 * self.hallucination_intensity)
            if time.time() - self.last_spawn > spawn_wait:
                # spawn 1 + intensity//2 hallucinations
                qty = 1 + int(self.hallucination_intensity // 2)
                for _ in range(qty):
                    self.spawn_hallucination()
                self.last_spawn = time.time()

            # move hallucinations
            for h in self.hallucinations:
                # flicker effect (they aren't always fully there)
                flick = (math.sin(time.time() * (1 + h['flicker'])) + 1) / 2  # 0..1
                # small random wobble
                h['vx'] += random.uniform(-0.06, 0.06)
                h['vy'] += random.uniform(-0.06, 0.06)
                h['x'] += h['vx']
                h['y'] += h['vy']
                # update canvas item
                alpha = 0.25 + 0.65 * flick  # not visible alpha in Tk — emulate with colors
                # darken or lighten fill to emulate flicker
                shade = int(20 + 120 * flick)
                col = "#{:02x}{:02x}{:02x}".format(min(255, shade), 8, 8)
                try:
                    self.canvas.coords(h['id'], h['x'] - 12, h['y'] - 12, h['x'] + 12, h['y'] + 12)
                    self.canvas.itemconfig(h['id'], fill=col)
                except Exception:
                    pass

            # handle collisions
            self.collide_player_with_pills()
            self.collide_player_with_hallucinations()

            # occasionally spawn a pill
            if random.random() < 0.004:
                self.spawn_pill()

            # update UI text
            self.canvas.itemconfigure(self.health_text, text=f"Health: {int(self.health)}/{self.max_health}")
            self.canvas.itemconfigure(self.drug_text, text=f"Pills (drugs): {self.drugs}   (D to use)")
            self.canvas.itemconfigure(self.score_text, text=f"Time survived: {int(self.score)}s")

            # visual distortion when hallucination_intensity high
            if self.hallucination_intensity >= 3:
                # subtle screen shake: shift canvas items randomly
                shake = int(min(12, 2 + self.hallucination_intensity * 2))
                tx = random.randint(-shake, shake)
                ty = random.randint(-shake, shake)
                self.canvas.move("all", tx, ty)
                # move back next tick
                def fix_shake():
                    self.canvas.move("all", -tx, -ty)
                self.win.after(60, fix_shake)

            # game over condition
            if self.health <= 0:
                self.health = 0
                self.game_over()
                return

        # schedule next tick (aim ~50 fps)
        self.win.after(20, self.tick)

    def game_over(self):
        self.running = False
        # show game over overlay
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black", stipple="gray75")
        self.canvas.create_text(self.width // 2, self.height // 2 - 30, text="YOU COULD NOT HOLD ON", fill="red", font=("Courier", 36))
        self.canvas.create_text(self.width // 2, self.height // 2 + 10, text=f"Time survived: {int(self.score)} seconds", fill="white", font=("Arial", 18))
        # play optional sound
        if AUDIO_AVAILABLE:
            try:
                s = pygame.mixer.Sound("death.wav")
                s.play()
            except Exception:
                pass
        # return to menu after short delay
        self.win.after(3000, self.end_game)

    def end_game(self):
        try:
            self.win.destroy()
        except Exception:
            pass
        if callable(self.on_game_close):
            try:
                self.on_game_close()
            except Exception:
                pass

# ---------- Run sequence ----------

if __name__ == "__main__":
    # hide initial root used for messagebox
    root = tk.Tk()
    root.withdraw()
    show_warning()