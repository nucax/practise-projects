import tkinter as tk
from tkinter import filedialog, Listbox, ttk
import pygame
import time
import threading
import os

pygame.mixer.init()

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("500x400")

        self.playlist = []
        self.current_index = -1
        self.playing = False
        self.paused = False

        # Playlist
        self.listbox = Listbox(root, width=60, height=10)
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-Button-1>", self.play_selected)

        # Controls
        controls_frame = tk.Frame(root)
        controls_frame.pack(pady=10)

        self.btn_prev = tk.Button(controls_frame, text="⏮ Prev", command=self.prev_song)
        self.btn_prev.grid(row=0, column=0, padx=5)

        self.btn_play = tk.Button(controls_frame, text="▶ Play", command=self.toggle_play)
        self.btn_play.grid(row=0, column=1, padx=5)

        self.btn_next = tk.Button(controls_frame, text="⏭ Next", command=self.next_song)
        self.btn_next.grid(row=0, column=2, padx=5)

        self.btn_stop = tk.Button(controls_frame, text="⏹ Stop", command=self.stop_song)
        self.btn_stop.grid(row=0, column=3, padx=5)

        # Progress bar
        self.progress = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=400)
        self.progress.pack(pady=10)

        # Volume slider
        self.volume = ttk.Scale(root, from_=0, to=1, orient="horizontal", value=0.5, command=self.set_volume)
        self.volume.pack(pady=5)
        pygame.mixer.music.set_volume(0.5)

        # Menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Add MP3(s)", command=self.load_files)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)

        # Thread to update progress bar
        self.update_thread = threading.Thread(target=self.update_progress, daemon=True)
        self.update_thread.start()

    def load_files(self):
        files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        for file in files:
            self.playlist.append(file)
            self.listbox.insert(tk.END, os.path.basename(file))

    def play_selected(self, event=None):
        index = self.listbox.curselection()
        if index:
            self.current_index = index[0]
            self.play_song()

    def play_song(self):
        if self.current_index >= 0 and self.current_index < len(self.playlist):
            song = self.playlist[self.current_index]
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
            self.btn_play.config(text="⏸ Pause")

    def toggle_play(self):
        if not self.playing:
            if self.current_index == -1 and self.playlist:
                self.current_index = 0
            self.play_song()
        elif self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.btn_play.config(text="⏸ Pause")
        else:
            pygame.mixer.music.pause()
            self.paused = True
            self.btn_play.config(text="▶ Play")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        self.btn_play.config(text="▶ Play")

    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_song()

    def prev_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_song()

    def set_volume(self, val):
        pygame.mixer.music.set_volume(float(val))

    def update_progress(self):
        while True:
            if self.playing and not self.paused:
                try:
                    pos = pygame.mixer.music.get_pos() / 1000  # seconds
                    self.progress.set(pos)
                except:
                    pass
            time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3Player(root)
    root.mainloop()
