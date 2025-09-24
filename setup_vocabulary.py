#!/usr/bin/env python3
"""
Script to populate comprehensive vocabulary database
Run this to set up all vocabulary with translations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comprehensive_vocabulary import populate_all_vocabulary
from translation_service import get_translator
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vocabulary_setup.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to set up comprehensive vocabulary"""
    logger.info("🚀 Starting comprehensive vocabulary setup...")
    
    try:
        # Initialize translator to check if models are working
        logger.info("Initializing translation service...")
        translator = get_translator()
        
        # Test translation
        test_translation = translator.translate_text("Hello", "hindi")
        logger.info(f"✅ Translation service working. Test: 'Hello' -> '{test_translation}'")
        
        # Populate vocabulary database
        logger.info("📚 Populating comprehensive vocabulary database...")
        success = populate_all_vocabulary()
        
        if success:
            logger.info("🎉 SUCCESS! Comprehensive vocabulary database populated successfully!")
            logger.info("📊 Database now contains:")
            logger.info("   • Hindi vowels and consonants")
            logger.info("   • Fruits and vegetables")
            logger.info("   • Animals and birds")
            logger.info("   • Colors")
            logger.info("   • Body parts")
            logger.info("   • Family relations")
            logger.info("   • Common greetings and phrases")
            logger.info("   • Translations in 15+ Indian languages")
            
            print("\n" + "="*60)
            print("✅ VOCABULARY SETUP COMPLETE!")
            print("🌍 VaaniMitra now supports translation to all Indian languages!")
            print("🎯 Users can learn from English to any supported language!")
            print("="*60)
            
        else:
            logger.error("❌ Failed to populate vocabulary database")
            return 1
            
    except Exception as e:
        logger.error(f"💥 Error during setup: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)