import tkinter as tk
import random
import time
import numpy as np
import simpleaudio as sa
import os
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource (works for dev and PyInstaller) """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

NOTE_NAMES = [
    'C4', 'Cs4', 'D4', 'Ds4', 'E4', 'F4', 'Fs4', 'G4', 'Gs4', 'A4', 'As4', 'B4',
    'C5', 'Cs5', 'D5'
]

NOTE_FILES = {note: resource_path(f"audio/{note}.wav") for note in NOTE_NAMES}
INTERVALS = [
    "Unison", "m2", "M2", "m3", "M3", "P4", "TT", "P5", "m6", "M6", "m7", "M7", "Octave"
]
CHORDS = {
    "Major": [0, 4, 7],
    "Minor": [0, 3, 7],
    "Diminished": [0, 3, 6],
    "Augmented": [0, 4, 8]
}
SCALES = {
    "Major": [0, 2, 4, 5, 7, 9, 11, 12],
    "Natural Minor": [0, 2, 3, 5, 7, 8, 10, 12],
    "Pentatonic": [0, 2, 4, 7, 9, 12]
}

def note_to_freq(note):
    note_names = ['C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B']
    octave = int(note[-1])
    key = note[:-1]
    n = note_names.index(key) + (octave - 4) * 12
    freq = 440 * (2 ** ((n - 9) / 12))  # A4 is the reference (n=9)
    return freq

def generate_tone(freq, duration=0.8):
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), False)
    tone = 0.5 * np.sin(freq * 2 * np.pi * t)
    tone = (tone * 32767).astype(np.int16)
    return sa.play_buffer(tone, 1, 2, fs)

def play_note(note, duration=0.8):
    print(f"Playing note: {note}")
    try:
        if note in NOTE_FILES and os.path.exists(NOTE_FILES[note]):
            wave_obj = sa.WaveObject.from_wave_file(NOTE_FILES[note])
            play_obj = wave_obj.play()
            play_obj.wait_done()
            return
    except Exception as e:
        print(f"Error playing {note}: {e}")
    freq = note_to_freq(note)
    print(f"Playing synthetic tone at {freq:.2f} Hz")
    play_obj = generate_tone(freq, duration)
    play_obj.wait_done()

def play_interval(start_index, interval):
    first_note = NOTE_NAMES[start_index]
    second_note = NOTE_NAMES[start_index + interval]
    print(f"Interval notes: {first_note}, {second_note}")
    play_note(first_note)
    time.sleep(0.4)
    play_note(second_note)
    return first_note, second_note

def play_chord(root_index, intervals):
    players = []
    notes = []
    for i in intervals:
        note = NOTE_NAMES[root_index + i]
        notes.append(note)
        print(f"Chord note: {note}")
        try:
            if note in NOTE_FILES and os.path.exists(NOTE_FILES[note]):
                wave_obj = sa.WaveObject.from_wave_file(NOTE_FILES[note])
                players.append(wave_obj.play())
                continue
        except:
            pass
        freq = note_to_freq(note)
        players.append(generate_tone(freq))
    time.sleep(1)
    for p in players:
        p.wait_done()
    return notes

def play_scale(root_index, intervals):
    notes = []
    for i in intervals:
        if root_index + i < len(NOTE_NAMES):
            note = NOTE_NAMES[root_index + i]
            notes.append(note)
            play_note(note)
            time.sleep(0.25)
    return notes

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 AI Music Trainer")
        self.root.configure(bg="#f0f0f0")
        self.root.geometry("1000x750")

        title = tk.Label(root, text="🎧 Ear Training", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
        title.pack(pady=20)

        btn_style = {"font": ("Helvetica", 12), "width": 30, "bg": "#e0e0e0", "relief": tk.RAISED, "bd": 3}

        tk.Button(root, text="▶ Play Random Interval", command=self.play_random_interval, **btn_style).pack(pady=10)
        tk.Button(root, text="▶ Play Random Chord", command=self.play_random_chord, **btn_style).pack(pady=10)
        tk.Button(root, text="▶ Play Random Scale", command=self.play_random_scale, **btn_style).pack(pady=10)

        self.output_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f0f0f0")
        self.output_label.pack(pady=20)

    def play_random_interval(self):
        interval = random.randint(1, 12)
        base = random.randint(0, len(NOTE_NAMES) - interval - 1)
        notes = play_interval(base, interval)
        self.output_label.config(text=f"Interval Played: {INTERVALS[interval]} ({notes[0]} → {notes[1]})")

    def play_random_chord(self):
        chord_name, intervals = random.choice(list(CHORDS.items()))
        root = random.randint(0, len(NOTE_NAMES) - max(intervals) - 1)
        notes = play_chord(root, intervals)
        self.output_label.config(text=f"Chord Played: {chord_name} ({', '.join(notes)})")

    def play_random_scale(self):
        scale_name, intervals = random.choice(list(SCALES.items()))
        root = random.randint(0, len(NOTE_NAMES) - max(intervals) - 1)
        notes = play_scale(root, intervals)
        self.output_label.config(text=f"Scale Played: {scale_name} ({' → '.join(notes)})")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()