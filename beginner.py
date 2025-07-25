from gtts import gTTS
import os
import pygame
from time import sleep

# List of Hindi vowels (Swar) and consonants (Vyanjan)
hindi_alphabets = [
    "अ", "आ", "इ", "ई", "उ", "ऊ", "ए", "ऐ", "ओ", "औ", "अं", "अः",  # Swar
    "क", "ख", "ग", "घ", "ङ",
    "च", "छ", "ज", "झ", "ञ",
    "ट", "ठ", "ड", "ढ", "ण",
    "त", "थ", "द", "ध", "न",
    "प", "फ", "ब", "भ", "म",
    "य", "र", "ल", "व",
    "श", "ष", "स", "ह",
    "क्ष", "त्र", "ज्ञ"
]

def speak_hindi(text):
    tts = gTTS(text=text, lang='hi')
    filename = "output.mp3"
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(0.1)
    pygame.mixer.quit()
    os.remove(filename)

def learn_hindi_alphabets():
    print("🔤 Let's Learn Hindi Alphabets with Pronunciation 🔊")
    for letter in hindi_alphabets:
        print(f"Alphabet: {letter}")
        speak_hindi(letter)
        input("Press Enter to continue to the next alphabet...")

if __name__ == "__main__":
    learn_hindi_alphabets()
