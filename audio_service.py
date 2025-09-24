"""
Audio Service for VaaniMitra
Handles text-to-speech generation and playback using Google TTS
"""

import os
import tempfile
import threading
import time
from gtts import gTTS
import pygame
import logging

logger = logging.getLogger(__name__)

class AudioService:
    def __init__(self):
        """Initialize pygame mixer for audio playback"""
        try:
            pygame.mixer.init()
            self.initialized = True
            logger.info("Audio service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize audio service: {e}")
            self.initialized = False
    
    def play_text_audio(self, text, language_code='hi', slow=False):
        """
        Generate and play audio for given text using Google TTS
        
        Args:
            text: Text to convert to speech
            language_code: Language code for TTS (hi=Hindi, gu=Gujarati, ta=Tamil, etc.)
            slow: Whether to speak slowly
            
        Returns:
            dict: Result of audio generation and playback
        """
        if not self.initialized:
            return {'success': False, 'error': 'Audio service not initialized'}
        
        temp_file = None
        try:
            # Generate TTS audio
            logger.info(f"Generating TTS for: '{text}' in language: {language_code}")
            tts = gTTS(text=text, lang=language_code, slow=slow)
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            tts.save(temp_file.name)
            temp_file.close()
            
            # Play audio
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            logger.info(f"Successfully played audio for: '{text}'")
            return {
                'success': True, 
                'message': f'Audio played for: {text}',
                'language': language_code
            }
            
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
            return {'success': False, 'error': str(e)}
        
        finally:
            # Clean up temporary file
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                    logger.debug(f"Cleaned up temp file: {temp_file.name}")
                except Exception as e:
                    logger.warning(f"Failed to clean up temp file: {e}")
    
    def play_letter_pronunciation(self, letter, target_language):
        """
        Play pronunciation of a letter in the target language
        
        Args:
            letter: The letter to pronounce (e.g., 'અ', 'आ', 'অ')
            target_language: Target language name (e.g., 'Gujarati', 'Hindi', 'Bengali')
            
        Returns:
            dict: Result of audio playback
        """
        # Map language names to TTS language codes
        language_map = {
            'hindi': 'hi',
            'gujarati': 'gu', 
            'tamil': 'ta',
            'bengali': 'bn',
            'telugu': 'te',
            'marathi': 'mr',
            'punjabi': 'pa',
            'urdu': 'ur',
            'english': 'en'
        }
        
        target_lang_lower = target_language.lower()
        language_code = language_map.get(target_lang_lower, 'hi')  # Default to Hindi
        
        logger.info(f"Playing letter '{letter}' in {target_language} (code: {language_code})")
        
        # For single letters, we might need to add context for better pronunciation
        # Some TTS services work better with syllables than isolated letters
        text_to_speak = letter
        
        return self.play_text_audio(text_to_speak, language_code, slow=True)
    
    def stop_audio(self):
        """Stop any currently playing audio"""
        if self.initialized:
            pygame.mixer.music.stop()
    
    def cleanup(self):
        """Cleanup audio resources"""
        if self.initialized:
            pygame.mixer.quit()

# Global audio service instance
audio_service = AudioService()

def play_letter_audio(letter, language):
    """
    Convenience function to play letter audio
    This can be called from Flask routes
    """
    return audio_service.play_letter_pronunciation(letter, language)

def play_text_audio(text, language):
    """
    Convenience function to play text audio
    """
    language_map = {
        'hindi': 'hi',
        'gujarati': 'gu', 
        'tamil': 'ta',
        'bengali': 'bn',
        'telugu': 'te',
        'marathi': 'mr',
        'punjabi': 'pa',
        'urdu': 'ur',
        'english': 'en'
    }
    
    target_lang_lower = language.lower()
    language_code = language_map.get(target_lang_lower, 'hi')
    
    return audio_service.play_text_audio(text, language_code)

# Cleanup function for app shutdown
def cleanup_audio():
    audio_service.cleanup()