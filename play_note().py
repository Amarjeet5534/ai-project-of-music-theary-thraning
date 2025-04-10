def play_note(note):
    if note in NOTE_FILES:
        try:
            print(f"Playing: {NOTE_FILES[note]}")  # Add this line
            wave_obj = sa.WaveObject.from_wave_file(NOTE_FILES[note])
            play_obj = wave_obj.play()
            play_obj.wait_done()
        except Exception as e:
            print(f"Error playing note {note}: {e}")
    else:
        print(f"Note file for {note} not found.")
