import simpleaudio as sa
import pygame

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1)

def test_simpleaudio():
    try:
        # Try playing a single note (C4) with simpleaudio
        wave_obj = sa.WaveObject.from_wave_file("audio/C4.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()
        print("✅ Playback successful with simpleaudio")
        return True
    except Exception as e:
        print(f"❌ Error with simpleaudio: {e}")
        return False

def test_pygame():
    try:
        # Try playing a single note (C4) with pygame
        pygame.mixer.music.load("audio/C4.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for sound to finish
            pygame.time.Clock().tick(10)
        print("✅ Playback successful with pygame")
        return True
    except Exception as e:
        print(f"❌ Error with pygame: {e}")
        return False

# Test both libraries
print("Testing playback with simpleaudio...")
simpleaudio_success = test_simpleaudio()

if not simpleaudio_success:
    print("\nTrying playback with pygame...")
    test_pygame()
