import tkinter as tk
import random
import time
import numpy as np
import simpleaudio as sa
import os
from pathlib import Path

# Note definitions
NOTE_NAMES = [
    'C4', 'Cs4', 'D4', 'Ds4', 'E4', 'F4', 'Fs4', 'G4', 'Gs4', 'A4', 'As4', 'B4',
    'C5', 'Cs5', 'D5'
]

# Create audio directory if it doesn't exist
audio_dir = Path("audio")
audio_dir.mkdir(exist_ok=True)

# Load note files that exist
NOTE_FILES = {}
for note in NOTE_NAMES:
    file_path = audio_dir / f"{note}.wav"
    if file_path.exists():
        NOTE_FILES[note] = str(file_path)
    else:
        print(f"Warning: Missing audio file for note {note}")

# Music theory definitions
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

class EarTraining:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.stats = {i: {"correct": 0, "wrong": 0} for i in range(13)}
        self.streak = 0
        self.max_streak = 0
        self.daily_goal = 10
        self.daily_progress = 0
        self.mistakes = []
        self.current_interval = 0
        self.base_index = 0
        self.note_index = 0
        self.chord_root = 0
        self.chord_type = ""
        self.scale_root = 0
        self.scale_type = ""

    def play_note(self, note):
        """Play a single note"""
        if note in NOTE_FILES:
            try:
                wave_obj = sa.WaveObject.from_wave_file(NOTE_FILES[note])
                return wave_obj.play()
            except Exception as e:
                print(f"Error playing note {note}: {e}")
        return None

    def play_interval(self, start_index, interval):
        """Play two notes with a delay between them"""
        self.play_note(NOTE_NAMES[start_index])
        if start_index + interval < len(NOTE_NAMES):
            self.root.after(400, lambda: self.play_note(NOTE_NAMES[start_index + interval]))

    def play_chord(self, root_index, intervals):
        """Play multiple notes simultaneously as a chord"""
        for i in intervals:
            if root_index + i < len(NOTE_NAMES):
                self.play_note(NOTE_NAMES[root_index + i])

    def play_scale(self, root_index, intervals):
        """Play notes sequentially with delays as a scale"""
        for i, interval in enumerate(intervals):
            if root_index + interval < len(NOTE_NAMES):
                self.root.after(250 * i, lambda i=i: self.play_note(NOTE_NAMES[root_index + intervals[i]]))

    def start(self):
        """Initialize the GUI"""
        self.clear()
        tk.Label(self.root, text="🎧 Full Ear Training Suite", font=("Helvetica", 16)).pack(pady=10)

        # Interval training section
        interval_frame = tk.LabelFrame(self.root, text="Intervals", padx=10, pady=5)
        interval_frame.pack(pady=5)
        tk.Button(interval_frame, text="▶ Play Interval", command=self.generate_interval).pack(pady=2)
        self.interval_feedback = tk.Label(interval_frame, text="")
        self.interval_feedback.pack()
        btn_frame = tk.Frame(interval_frame)
        btn_frame.pack()
        for i, name in enumerate(INTERVALS):
            btn = tk.Button(btn_frame, text=name, width=6, command=lambda i=i: self.check_interval(i))
            btn.grid(row=i//7, column=i%7, padx=2, pady=2)

        # Note training section
        note_frame = tk.LabelFrame(self.root, text="Notes", padx=10, pady=5)
        note_frame.pack(pady=5)
        tk.Button(note_frame, text="▶ Play Note", command=self.generate_note).pack(pady=2)
        self.note_feedback = tk.Label(note_frame, text="")
        self.note_feedback.pack()
        grid = tk.Frame(note_frame)
        grid.pack()
        for i, note in enumerate(NOTE_NAMES):
            btn = tk.Button(grid, text=note, width=4, command=lambda i=i: self.check_note(i))
            btn.grid(row=i//8, column=i%8, padx=2, pady=2)

        # Chord training section
        chord_frame = tk.LabelFrame(self.root, text="Chords", padx=10, pady=5)
        chord_frame.pack(pady=5)
        tk.Button(chord_frame, text="▶ Play Chord", command=self.generate_chord).pack(pady=2)
        self.chord_feedback = tk.Label(chord_frame, text="")
        self.chord_feedback.pack()
        chord_btns = tk.Frame(chord_frame)
        chord_btns.pack()
        for name in CHORDS:
            tk.Button(chord_btns, text=name, width=10, command=lambda n=name: self.check_chord(n)).pack(side=tk.LEFT, padx=5)

        # Scale training section
        scale_frame = tk.LabelFrame(self.root, text="Scales", padx=10, pady=5)
        scale_frame.pack(pady=5)
        tk.Button(scale_frame, text="▶ Play Scale", command=self.generate_scale).pack(pady=2)
        self.scale_feedback = tk.Label(scale_frame, text="")
        self.scale_feedback.pack()
        scale_btns = tk.Frame(scale_frame)
        scale_btns.pack()
        for name in SCALES:
            tk.Button(scale_btns, text=name, width=15, command=lambda n=name: self.check_scale(n)).pack(side=tk.LEFT, padx=5)

        # Additional features
        extra_frame = tk.Frame(self.root)
        extra_frame.pack(pady=10)
        for text, cmd in [
            ("🏆 Achievements", self.achievements),
            ("🤖 AI Difficulty", self.ai_difficulty),
            ("📊 Advanced Stats", self.advanced_stats),
            ("🔥 Streak & Daily Goal", self.show_streak_and_goal),
            ("🔁 Mistake Review", self.review_mistakes)
        ]:
            tk.Button(extra_frame, text=text, width=25, command=cmd).pack(pady=2)

        tk.Button(self.root, text="⬅ Back to Menu", command=self.back_callback).pack(pady=10)

    def clear(self):
        """Clear all widgets from the root"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def generate_interval(self):
        """Generate a random interval to identify"""
        weights = [(self.stats[i]['wrong'] + 1) / (self.stats[i]['correct'] + 1) for i in range(13)]
        self.current_interval = np.random.choice(range(13), p=np.array(weights)/sum(weights))
        self.base_index = random.randint(0, len(NOTE_NAMES) - self.current_interval - 1)
        self.play_interval(self.base_index, self.current_interval)
        self.interval_feedback.config(text="Interval played.")

    def check_interval(self, guess):
        """Check if the interval guess was correct"""
        if guess == self.current_interval:
            self.stats[guess]['correct'] += 1
            self.streak += 1
            self.max_streak = max(self.streak, self.max_streak)
            self.daily_progress += 1
            self.interval_feedback.config(text="✅ Correct!")
        else:
            self.stats[self.current_interval]['wrong'] += 1
            self.streak = 0
            self.mistakes.append(self.current_interval)
            self.interval_feedback.config(text=f"❌ Wrong! It was: {INTERVALS[self.current_interval]}")

    def generate_note(self):
        """Generate a random note to identify"""
        self.note_index = random.randint(0, len(NOTE_NAMES) - 1)
        self.play_note(NOTE_NAMES[self.note_index])
        self.note_feedback.config(text="Note played.")

    def check_note(self, guess):
        """Check if the note guess was correct"""
        result = "✅ Correct!" if guess == self.note_index else f"❌ Wrong! It was {NOTE_NAMES[self.note_index]}"
        self.note_feedback.config(text=result)

    def generate_chord(self):
        """Generate a random chord to identify"""
        self.chord_root = random.randint(0, len(NOTE_NAMES) - 8)
        self.chord_type = random.choice(list(CHORDS.keys()))
        self.play_chord(self.chord_root, CHORDS[self.chord_type])
        self.chord_feedback.config(text="Chord played.")

    def check_chord(self, guess):
        """Check if the chord guess was correct"""
        result = "✅ Correct!" if guess == self.chord_type else f"❌ Wrong! It was {self.chord_type}"
        self.chord_feedback.config(text=result)

    def generate_scale(self):
        """Generate a random scale to identify"""
        self.scale_root = random.randint(0, len(NOTE_NAMES) - 13)
        self.scale_type = random.choice(list(SCALES.keys()))
        self.play_scale(self.scale_root, SCALES[self.scale_type])
        self.scale_feedback.config(text="Scale played.")

    def check_scale(self, guess):
        """Check if the scale guess was correct"""
        result = "✅ Correct!" if guess == self.scale_type else f"❌ Wrong! It was {self.scale_type}"
        self.scale_feedback.config(text=result)

    def achievements(self):
        """Show achievements based on performance"""
        correct_total = sum(v['correct'] for v in self.stats.values())
        if correct_total >= 50:
            msg = "🏅 Master Listener: 50+ correct answers!"
        elif correct_total >= 20:
            msg = "🎖 Skilled Ear: 20+ correct answers!"
        elif correct_total >= 10:
            msg = "🔰 Beginner Badge: 10+ correct answers!"
        else:
            msg = "🚀 Keep practicing for achievements!"
        self.interval_feedback.config(text=msg)

    def ai_difficulty(self):
        """Show which interval is most challenging"""
        hardest = max(self.stats.items(), key=lambda x: x[1]['wrong'] - x[1]['correct'])[0]
        self.interval_feedback.config(text=f"🤖 Focus on: {INTERVALS[hardest]} (based on performance)")

    def advanced_stats(self):
        """Show detailed statistics"""
        total = sum(self.stats[i]['correct'] + self.stats[i]['wrong'] for i in self.stats)
        correct = sum(self.stats[i]['correct'] for i in self.stats)
        accuracy = (correct / total * 100) if total > 0 else 0
        lines = [f"📊 Stats — Total: {total}, Correct: {correct}, Accuracy: {accuracy:.1f}%"]
        for i in self.stats:
            attempts = self.stats[i]['correct'] + self.stats[i]['wrong']
            if attempts:
                acc = self.stats[i]['correct'] / attempts * 100
                lines.append(f"{INTERVALS[i]}: {self.stats[i]['correct']}/{attempts} ({acc:.0f}%)")
        self.interval_feedback.config(text="\n".join(lines))

    def show_streak_and_goal(self):
        """Show current streak and daily progress"""
        self.interval_feedback.config(text=f"🔥 Streak: {self.streak} (Max: {self.max_streak})\n🎯 Daily Progress: {self.daily_progress}/{self.daily_goal}")

    def review_mistakes(self):
        """Review previously mistaken intervals"""
        if not self.mistakes:
            self.interval_feedback.config(text="✅ No mistakes to review!")
        else:
            interval = self.mistakes.pop(0)
            self.current_interval = interval
            self.base_index = random.randint(0, len(NOTE_NAMES) - interval - 1)
            self.play_interval(self.base_index, interval)
            self.interval_feedback.config(text=f"🔁 Reviewing: {INTERVALS[interval]}")

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Music Theory Trainer")
        self.show_main_menu()

    def show_main_menu(self):
        """Show the main menu screen"""
        self.clear()
        tk.Label(self.root, text="🎵 AI Music Theory Trainer", font=("Helvetica", 18)).pack(pady=20)
        tk.Button(self.root, text="🎧 Start Ear Training", width=30, command=self.start_ear_training).pack(pady=5)
        tk.Button(self.root, text="❌ Exit", width=30, command=self.root.quit).pack(pady=5)

    def start_ear_training(self):
        """Start the ear training module"""
        self.trainer = EarTraining(self.root, self.show_main_menu)
        self.trainer.start()

    def clear(self):
        """Clear all widgets from the root"""
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    root.geometry("1000x750")
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
