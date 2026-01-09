"""
VaaniMitra Translation Service
Now uses MongoDB database for all translations (no AI model loading)
Provides backward compatibility with old IndicTrans2Service interface
"""

import logging
from db_translation_service import db_translation_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndicTrans2Service:
    """
    Translation service wrapper for backward compatibility
    Delegates all translation work to DatabaseTranslationService
    No AI model loading - purely database-driven
    """
    
    def __init__(self):
        """Initialize with database translation service"""
        self.db_service = db_translation_service
        self.supported_languages = self.db_service.supported_languages
        logger.info("Translation Service initialized (using MongoDB database)")
    
    def translate_text(self, text, target_language):
        """
        Translate English text to target Indian language
        
        Args:
            text (str): English text to translate
            target_language (str): Target language name
        
        Returns:
            str: Translated text from database or original if not found
        """
        return self.db_service.translate_text(text, target_language)
    
    def batch_translate(self, texts, target_language):
        """
        Translate multiple texts at once
        
        Args:
            texts (list): List of English texts
            target_language (str): Target language name
        
        Returns:
            list: List of translated texts
        """
        return self.db_service.batch_translate(texts, target_language)
    
    def translate_vocabulary_category(self, category, target_language):
        """
        Translate an entire vocabulary category
        
        Args:
            category (str): Category name (fruits, animals, etc.)
            target_language (str): Target language name
        
        Returns:
            list: List of translation objects with english/translated fields
        """
        return self.db_service.get_translations_by_category(category, target_language)
    
    def get_all_available_categories(self):
        """Get all vocabulary categories"""
        from native_content_system import get_all_vocabulary_categories
        return get_all_vocabulary_categories()
    
    def add_translation(self, english_word, target_language, translation):
        """
        Add or update a translation
        
        Args:
            english_word (str): English word
            target_language (str): Target language
            translation (str): Translated text
        
        Returns:
            bool: Success status
        """
        return self.db_service.add_translation(english_word, target_language, translation)

# Helper functions for translation_routes.py compatibility
def get_translator():
    """
    Get translator instance
    
    Returns:
        IndicTrans2Service: Translator instance
    """
    return IndicTrans2Service()

def translate_vocabulary_data(vocabulary_data, target_language):
    """
    Translate vocabulary data from English to target language
    
    Args:
        vocabulary_data (list): List of vocabulary items with 'english' field
        target_language (str): Target language name
    
    Returns:
        list: List of translated vocabulary items
    """
    translator = get_translator()
    translated_data = []
    
    for item in vocabulary_data:
        english = item.get('english', '')
        if english:
            translated = translator.translate_text(english, target_language)
        else:
            translated = ''
        
        translated_item = item.copy()
        translated_item['translated'] = translated
        translated_item['target_language'] = target_language
        translated_data.append(translated_item)
    
    logger.info(f"Translated {len(translated_data)} vocabulary items to {target_language}")
    return translated_data

# Global service instance
translation_service = IndicTrans2Service()
