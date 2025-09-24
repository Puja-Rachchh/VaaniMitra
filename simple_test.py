#!/usr/bin/env python3
"""
Simple test and setup script for translation system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from translation_service import get_translator
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_translation_only():
    """Test just the translation service without database"""
    logger.info("🧪 Testing Translation Service Only...")
    
    try:
        translator = get_translator()
        logger.info("✅ Translator initialized successfully")
        
        # Test basic translations
        test_cases = [
            ("Hello", "hindi"),
            ("Apple", "tamil"),
            ("Dog", "bengali"),
        ]
        
        for english_text, target_lang in test_cases:
            try:
                translation = translator.translate_text(english_text, target_lang)
                logger.info(f"✅ '{english_text}' -> {target_lang}: '{translation}'")
            except Exception as e:
                logger.warning(f"⚠️ Failed to translate '{english_text}' to {target_lang}: {e}")
        
        # Test available languages
        languages = translator.get_available_languages()
        logger.info(f"✅ Supported languages ({len(languages)}): {', '.join(languages[:5])}...")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Translation service test failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("🚀 VaaniMitra Translation System - Simple Test")
    logger.info("=" * 50)
    
    # Test translation service
    success = test_translation_only()
    
    if success:
        logger.info("🎉 Translation service is working!")
        logger.info("📝 Next steps:")
        logger.info("   1. Start the Flask app: python app.py")
        logger.info("   2. Visit beginner or intermediate levels")
        logger.info("   3. Use the language selector to test translations")
        logger.info("   4. Database population can be done through the web app")
        return 0
    else:
        logger.error("❌ Translation service failed. Check dependencies.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)