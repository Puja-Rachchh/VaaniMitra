from gtts import gTTS
import os
import pygame
from time import sleep
import tempfile

def speak_hindi(text):
    # Create a temporary file in the system's temp directory
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
        filename = temp_file.name
        
    # Generate and save audio
    tts = gTTS(text=text, lang='hi')
    tts.save(filename)
    
    # Play the audio
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(0.1)
    pygame.mixer.quit()
    
    # Clean up the temporary file
    os.remove(filename)

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
