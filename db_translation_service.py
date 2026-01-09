"""
Database Translation Service
Fetches all translations from MongoDB database
No AI model loading - purely database-driven
"""

import logging
from mongodb_models import mongo
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseTranslationService:
    """Translation service that uses pre-populated MongoDB database"""
    
    def __init__(self):
        """Initialize database translation service"""
        self.supported_languages = [
            'hindi', 'gujarati', 'tamil', 'bengali', 'telugu', 
            'marathi', 'punjabi', 'urdu', 'kannada', 'malayalam',
            'odia', 'assamese', 'nepali'
        ]
        logger.info("Database Translation Service initialized")
    
    def translate_text(self, text, target_language):
        """
        Translate English text to target Indian language by fetching from MongoDB
        
        Args:
            text (str): English text to translate
            target_language (str): Target language name
        
        Returns:
            str: Translated text or original text if not found
        """
        if not text:
            return text
        
        # Normalize inputs
        text_lower = text.lower().strip()
        language_lower = target_language.lower().strip()
        
        # Validate language
        if language_lower not in self.supported_languages:
            logger.warning(f"Unsupported language: {target_language}")
            return text
        
        try:
            # Query MongoDB for translation
            translation_doc = mongo.db.translations.find_one({
                'english': text_lower,
                'language': language_lower
            })
            
            if translation_doc and translation_doc.get('translation'):
                translated = translation_doc['translation']
                logger.info(f"Found translation: '{text}' -> '{translated}' ({target_language})")
                return translated
            else:
                logger.warning(f"No translation found for '{text}' in {target_language}")
                return text
                
        except Exception as e:
            logger.error(f"Database error while translating '{text}' to {target_language}: {e}")
            return text
    
    def get_all_translations_for_language(self, target_language):
        """
        Get all available translations for a specific language
        
        Args:
            target_language (str): Target language name
        
        Returns:
            dict: Dictionary mapping English words to translations
        """
        language_lower = target_language.lower().strip()
        
        if language_lower not in self.supported_languages:
            logger.warning(f"Unsupported language: {target_language}")
            return {}
        
        try:
            translations = mongo.db.translations.find({'language': language_lower})
            
            translation_dict = {}
            for doc in translations:
                english = doc.get('english', '')
                translated = doc.get('translation', '')
                if english and translated:
                    translation_dict[english] = translated
            
            logger.info(f"Retrieved {len(translation_dict)} translations for {target_language}")
            return translation_dict
            
        except Exception as e:
            logger.error(f"Database error while fetching translations for {target_language}: {e}")
            return {}
    
    def get_translations_by_category(self, category, target_language):
        """
        Get translations for a specific category (fruits, animals, etc.)
        
        Args:
            category (str): Category name
            target_language (str): Target language name
        
        Returns:
            list: List of translation objects
        """
        from native_content_system import get_english_vocabulary
        
        # Get English words for this category
        english_words = get_english_vocabulary(category)
        if not english_words:
            logger.warning(f"No vocabulary found for category '{category}'")
            return []
        
        language_lower = target_language.lower().strip()
        
        if language_lower not in self.supported_languages:
            logger.warning(f"Unsupported language: {target_language}")
            return []
        
        try:
            # Get translations for all words in category
            translations = []
            for english_word in english_words:
                translated = self.translate_text(english_word, target_language)
                
                translations.append({
                    'english': english_word,
                    'translated': translated,
                    'category': category,
                    'target_language': target_language
                })
            
            logger.info(f"Retrieved {len(translations)} translations for category '{category}' in {target_language}")
            return translations
            
        except Exception as e:
            logger.error(f"Error getting translations for category '{category}': {e}")
            return []
    
    def batch_translate(self, texts, target_language):
        """
        Translate multiple texts at once
        
        Args:
            texts (list): List of English texts to translate
            target_language (str): Target language name
        
        Returns:
            list: List of translated texts
        """
        if not texts:
            return []
        
        language_lower = target_language.lower().strip()
        
        if language_lower not in self.supported_languages:
            logger.warning(f"Unsupported language: {target_language}")
            return texts
        
        try:
            # Prepare query for batch lookup
            text_lower_list = [t.lower().strip() for t in texts]
            
            # Query MongoDB for all translations
            translation_docs = mongo.db.translations.find({
                'english': {'$in': text_lower_list},
                'language': language_lower
            })
            
            # Create mapping
            translation_map = {}
            for doc in translation_docs:
                english = doc.get('english', '')
                translated = doc.get('translation', '')
                if english and translated:
                    translation_map[english] = translated
            
            # Build result list maintaining order
            results = []
            for original_text in texts:
                text_lower = original_text.lower().strip()
                translated = translation_map.get(text_lower, original_text)
                results.append(translated)
            
            logger.info(f"Batch translated {len(results)} texts to {target_language}")
            return results
            
        except Exception as e:
            logger.error(f"Database error in batch translation to {target_language}: {e}")
            return texts
    
    def add_translation(self, english_word, target_language, translation):
        """
        Add or update a translation in the database
        
        Args:
            english_word (str): English word
            target_language (str): Target language
            translation (str): Translated text
        
        Returns:
            bool: Success status
        """
        english_lower = english_word.lower().strip()
        language_lower = target_language.lower().strip()
        
        if language_lower not in self.supported_languages:
            logger.warning(f"Unsupported language: {target_language}")
            return False
        
        try:
            translation_doc = {
                'english': english_lower,
                'language': language_lower,
                'translation': translation,
                'verified': False,  # Mark as unverified since it's user-added
                'updated_at': datetime.utcnow()
            }
            
            # Update if exists, insert if new
            result = mongo.db.translations.update_one(
                {'english': english_lower, 'language': language_lower},
                {'$set': translation_doc, '$setOnInsert': {'created_at': datetime.utcnow()}},
                upsert=True
            )
            
            if result.upserted_id:
                logger.info(f"Added new translation: '{english_word}' -> '{translation}' ({target_language})")
            else:
                logger.info(f"Updated translation: '{english_word}' -> '{translation}' ({target_language})")
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding/updating translation: {e}")
            return False
    
    def get_translation_stats(self):
        """
        Get statistics about translations in database
        
        Returns:
            dict: Statistics about translations
        """
        try:
            stats = {}
            
            # Total translations
            total = mongo.db.translations.count_documents({})
            stats['total_translations'] = total
            
            # Per language counts
            stats['by_language'] = {}
            for language in self.supported_languages:
                count = mongo.db.translations.count_documents({'language': language})
                stats['by_language'][language] = count
            
            # Verified vs unverified
            verified = mongo.db.translations.count_documents({'verified': True})
            unverified = mongo.db.translations.count_documents({'verified': False})
            stats['verified'] = verified
            stats['unverified'] = unverified
            
            logger.info(f"Translation stats: {total} total, {verified} verified, {unverified} unverified")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting translation stats: {e}")
            return {}

# Global service instance
db_translation_service = DatabaseTranslationService()
