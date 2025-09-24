"""
VaaniMitra Translation Service using IndicTrans2
Automated translation for all Indian languages
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndicTrans2Service:
    def __init__(self):
        """Initialize IndicTrans2 model for translation"""
        self.model_name = "ai4bharat/indictrans2-en-indic-dist-200M"  # Use smaller model
        self.device = "cpu"  # Force CPU to avoid memory issues
        self.cache_dir = "E:/VaaniMitraData/models"  # Use E drive cache
        
        # Tamil fallback translations for common words
        self.fallback_translations = {
            'tamil': {
                'red': 'சிவப்பு',
                'blue': 'நீலம்',
                'green': 'பச்சை',
                'yellow': 'மஞ்சள்',
                'orange': 'ஆரஞ்சு',
                'purple': 'ஊதா',
                'pink': 'இளஞ்சிவப்பு',
                'brown': 'பழுப்பு',
                'black': 'கருப்பு',
                'white': 'வெள்ளை',
                'gray': 'சாம்பல்',
                'cyan': 'சியான்',
                'violet': 'ஊதா நிறம்',
                'indigo': 'இண்டிகோ',
                'magenta': 'மெஜெண்டா',
                'maroon': 'மெரூன்',
                'navy': 'கடற்படை நீலம்',
                'olive': 'ஆலிவ்',
                'silver': 'வெள்ளி',
                'gold': 'தங்கம்',
                # Animals
                'dog': 'நாய்',
                'cat': 'பூனை',
                'cow': 'பசு',
                'horse': 'குதிரை',
                'elephant': 'யானை',
                'tiger': 'புலி',
                'lion': 'சிங்கம்',
                'monkey': 'குரங்கு',
                'bear': 'கரடி',
                'fox': 'நரி',
                'rabbit': 'முயல்',
                'deer': 'மான்',
                'goat': 'ஆடு',
                'sheep': 'செம்மறி ஆடு',
                'pig': 'பன்றி',
                'duck': 'வாத்து',
                'chicken': 'கோழி',
                'peacock': 'மயில்',
                'parrot': 'கிளி',
                'eagle': 'கழுகு',
                'snake': 'பாம்பு',
                'frog': 'தவளை',
                'fish': 'மீன்',
                'butterfly': 'பட்டாம்பூச்சி',
                'ant': 'எறும்பு',
                'bee': 'தேனீ',
                # Vegetables
                'tomato': 'தக்காளி',
                'onion': 'வெங்காயம்',
                'potato': 'உருளைக்கிழங்கு',
                'carrot': 'கேரட்',
                'beans': 'பீன்ஸ்',
                'cabbage': 'முட்டைகோஸ்',
                'cauliflower': 'காலிஃப்ளவர்',
                'brinjal': 'கத்தரிக்காய்',
                'okra': 'வென்டைக்காய்',
                'cucumber': 'வெள்ளரிக்காய்',
                'spinach': 'கீரை',
                'chili': 'மிளகாய்',
                'ginger': 'இஞ்சி',
                'garlic': 'பூண்டு',
                'pumpkin': 'பூசணிக்காய்',
            }
        }
        
        # Language mapping for Indian languages
        self.supported_languages = {
            'english': 'eng_Latn',
            'hindi': 'hin_Deva',
            'bengali': 'ben_Beng',
            'gujarati': 'guj_Gujr',
            'kannada': 'kan_Knda',
            'malayalam': 'mal_Mlym',
            'marathi': 'mar_Deva',
            'oriya': 'ori_Orya',
            'punjabi': 'pan_Guru',
            'tamil': 'tam_Taml',
            'telugu': 'tel_Telu',
            'urdu': 'urd_Arab',
            'assamese': 'asm_Beng',
            'konkani': 'kok_Deva',
            'maithili': 'mai_Deva',
            'nepali': 'npi_Deva',
            'sanskrit': 'san_Deva',
            'sindhi': 'snd_Deva',
            'bodo': 'brx_Deva',
            'dogri': 'doi_Deva',
            'kashmiri': 'kas_Deva',
            'manipuri': 'mni_Mtei',
            'santali': 'sat_Olck'
        }
        
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load IndicTrans2 model and tokenizer"""
        try:
            logger.info("Loading IndicTrans2 model...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, 
                trust_remote_code=True,
                cache_dir=self.cache_dir
            )
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_name, 
                trust_remote_code=True,
                torch_dtype=torch.float32,  # Use float32 to reduce memory
                cache_dir=self.cache_dir
            ).to(self.device)
            logger.info(f"Model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            # Don't raise exception, allow service to work with fallbacks only
            self.model = None
            self.tokenizer = None
            logger.warning("Model loading failed, will use fallback translations only")
    
    def translate_text(self, text, target_language):
        """
        Translate English text to specified Indian language
        
        Args:
            text (str): English text to translate
            target_language (str): Target language name (e.g., 'hindi', 'tamil')
        
        Returns:
            str: Translated text or original text if translation fails
        """
        if not text:
            return text
            
        # Make language check case-insensitive
        target_lang_lower = target_language.lower()
        if target_lang_lower not in self.supported_languages:
            return text

        # Check for fallback translation first
        fallback_result = self._get_fallback_translation(text, target_language)
        if fallback_result:
            logger.info(f"Using fallback translation for '{text}': '{fallback_result}'")
            return fallback_result

        # Check if model is loaded
        if not self.model or not self.tokenizer:
            logger.warning(f"Model not loaded, cannot translate '{text}' to {target_language}")
            return text

        # If model is not loaded, return fallback or original
        if not self.model or not self.tokenizer:
            logger.warning(f"Model not available, returning original text for '{text}'")
            return text

        try:
            # Get language code - make lookup case-insensitive
            lang_code = self.supported_languages[target_lang_lower]
            
            # Create proper IndicTrans2 input format
            input_text = f"eng_Latn {lang_code} {text}"
            
            # Tokenize
            inputs = self.tokenizer(
                input_text, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=256
            ).to(self.device)
            
            # Generate translation
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=256,
                    num_beams=2,
                    length_penalty=0.6,
                    early_stopping=True,
                    do_sample=False
                )
            
            # Decode output
            full_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the translation part - IndicTrans2 format: "eng_Latn tam_Taml text" -> translated_text
            translated = None
            
            # Remove the input format prefix to get the translation
            input_prefix = f"eng_Latn {lang_code} {text}"
            if input_prefix in full_output:
                translated = full_output.replace(input_prefix, "").strip()
            else:
                # Fallback: just remove the language codes and original text
                translated = full_output.replace("eng_Latn", "").replace(lang_code, "").replace(text, "").strip()
            
            # Clean up any remaining artifacts
            if translated:
                translated = translated.strip()
                # Remove any leading/trailing punctuation artifacts
                while translated and translated[0] in '.,;:!?':
                    translated = translated[1:].strip()
            
            # Validate the translation for correct script
            if translated and translated != text and self._is_valid_translation(translated, target_language):
                logger.info(f"Translated '{text}' to {target_language}: '{translated}'")
                return translated
            else:
                # Try fallback if translation is invalid
                fallback_result = self._get_fallback_translation(text, target_language)
                if fallback_result:
                    logger.info(f"Using fallback translation for '{text}': '{fallback_result}'")
                    return fallback_result
                
                # If no fallback, return original
                logger.warning(f"No valid translation found for '{text}' to {target_language}, returning original")
                return text
            
        except Exception as e:
            logger.error(f"Translation failed for '{text}' to {target_language}: {e}")
            # Try fallback on error
            fallback_result = self._get_fallback_translation(text, target_language)
            if fallback_result:
                return fallback_result
            return text

    def _get_fallback_translation(self, text, target_language):
        """Get fallback translation from manual mapping"""
        # Make language lookup case-insensitive
        target_lang_lower = target_language.lower()
        if target_lang_lower in self.fallback_translations:
            return self.fallback_translations[target_lang_lower].get(text.lower())
        return None

    def _is_valid_translation(self, translation, target_language):
        """Check if the translation is in the correct script for the target language"""
        if not translation:
            return False
            
        # Check for wrong script issues - make language check case-insensitive
        if target_language.lower() == 'tamil':
            # Tamil should contain Tamil script characters (U+0B80-U+0BFF)
            # If it contains Devanagari characters (U+0900-U+097F), it's wrong
            has_tamil = any('\u0b80' <= char <= '\u0bff' for char in translation)
            has_devanagari = any('\u0900' <= char <= '\u097f' for char in translation)
            
            # For Tamil, we MUST have Tamil script and NO Devanagari
            if has_devanagari or not has_tamil:
                logger.warning(f"Invalid Tamil translation '{translation}' - contains Devanagari or missing Tamil script")
                return False
            return True
            
        # For other languages, assume valid for now
        return True
    
    def translate_batch(self, texts, target_language):
        """
        Translate multiple texts to target language
        
        Args:
            texts (list): List of English texts
            target_language (str): Target language name
        
        Returns:
            list: List of translated texts
        """
        if not texts or target_language not in self.supported_languages:
            return texts
        
        translations = []
        for text in texts:
            translation = self.translate_text(text, target_language)
            translations.append(translation)
        
        return translations
    
    def get_available_languages(self):
        """Get list of supported languages"""
        return list(self.supported_languages.keys())
    
    def translate_vocabulary(self, vocabulary_dict, target_languages=None):
        """
        Translate vocabulary dictionary to multiple languages
        
        Args:
            vocabulary_dict (dict): Dictionary with English words/phrases
            target_languages (list): List of target languages, if None uses all supported
        
        Returns:
            dict: Multi-language vocabulary dictionary
        """
        if target_languages is None:
            target_languages = self.get_available_languages()
        
        multi_lang_vocab = {}
        
        for category, items in vocabulary_dict.items():
            multi_lang_vocab[category] = {}
            
            for item_key, item_data in items.items():
                multi_lang_vocab[category][item_key] = {
                    'english': item_data.get('english', item_key),
                    'translations': {}
                }
                
                # Translate to each target language
                english_text = item_data.get('english', item_key)
                for lang in target_languages:
                    if lang != 'english':  # Skip English as it's source
                        translation = self.translate_text(english_text, lang)
                        multi_lang_vocab[category][item_key]['translations'][lang] = translation
        
        return multi_lang_vocab

    def translate_level_content(self, content_dict, target_language):
        """Translate level content (instructions, titles, etc.)"""
        try:
            translated_content = {}
            
            for key, value in content_dict.items():
                if isinstance(value, str):
                    translated_content[key] = self.translate_text(value, target_language)
                elif isinstance(value, dict):
                    # Recursively translate nested dictionaries
                    translated_content[key] = self.translate_level_content(value, target_language)
                elif isinstance(value, list):
                    # Translate list items if they are strings
                    translated_content[key] = [
                        self.translate_text(item, target_language) if isinstance(item, str) else item
                        for item in value
                    ]
                else:
                    # Keep non-string values as is
                    translated_content[key] = value
            
            return translated_content
            
        except Exception as e:
            logger.error(f"Error translating level content: {e}")
            return content_dict

    def translate_vocabulary_category(self, category, target_language):
        """
        Translate an entire vocabulary category from English to target language
        Uses native_content_system.py for English vocabulary
        """
        try:
            from native_content_system import get_english_vocabulary
            
            # Get English words for this category from native_content_system
            english_words = get_english_vocabulary(category)
            if not english_words:
                logger.warning(f"No vocabulary found for category '{category}'")
                return []
            
            logger.info(f"Translating {len(english_words)} words from '{category}' category to {target_language}")
            
            # Translate each word
            translated_vocabulary = []
            successful_translations = 0
            failed_translations = 0
            
            for i, english_word in enumerate(english_words):
                try:
                    logger.info(f"Translating word {i+1}/{len(english_words)}: '{english_word}'")
                    translated_word = self.translate_text(english_word, target_language)
                    
                    # Check if translation is valid (not the same as original)
                    if translated_word and translated_word != english_word:
                        successful_translations += 1
                        logger.info(f"✓ Successfully translated '{english_word}' -> '{translated_word}'")
                    else:
                        failed_translations += 1
                        logger.warning(f"✗ Translation failed or returned same for '{english_word}': '{translated_word}'")
                        translated_word = english_word  # Fallback to English
                    
                    vocab_item = {
                        'english': english_word,
                        'translated': translated_word,
                        'category': category,
                        'target_language': target_language
                    }
                    translated_vocabulary.append(vocab_item)
                    
                except Exception as e:
                    failed_translations += 1
                    logger.error(f"Error translating '{english_word}': {str(e)}")
                    # Add untranslated word as fallback
                    vocab_item = {
                        'english': english_word,
                        'translated': english_word,  # Fallback to English
                        'category': category,
                        'target_language': target_language
                    }
                    translated_vocabulary.append(vocab_item)
            
            logger.info(f"Translation summary: {successful_translations} successful, {failed_translations} failed out of {len(english_words)} total")
            logger.info(f"Successfully translated {len(translated_vocabulary)} words for category '{category}'")
            return translated_vocabulary
            
        except Exception as e:
            logger.error(f"Error translating vocabulary category '{category}' to {target_language}: {str(e)}")
            # Return English words as fallback
            from native_content_system import get_english_vocabulary
            english_words = get_english_vocabulary(category)
            fallback_vocabulary = []
            for word in english_words:
                fallback_vocabulary.append({
                    'english': word,
                    'translated': word,
                    'category': category,
                    'target_language': target_language
                })
            return fallback_vocabulary

    def get_level_vocabulary(self, level, language='english'):
        """Get vocabulary for a specific level in the target language"""
        try:
            from comprehensive_vocabulary import get_vocabulary_for_level
            return get_vocabulary_for_level(level, language)
        except Exception as e:
            logger.error(f"Error getting level vocabulary: {e}")
            return {}

    def translate_quiz_questions(self, questions, target_language):
        """Translate quiz questions and options"""
        try:
            translated_questions = []
            
            for question in questions:
                translated_question = question.copy()
                
                # Translate question text
                if 'question' in question:
                    translated_question['question'] = self.translate_text(question['question'], target_language)
                
                # Translate options
                if 'options' in question:
                    translated_question['options'] = [
                        self.translate_text(option, target_language) 
                        for option in question['options']
                    ]
                
                # Translate correct answer
                if 'correct_answer' in question:
                    translated_question['correct_answer'] = self.translate_text(question['correct_answer'], target_language)
                
                # Translate explanation if exists
                if 'explanation' in question:
                    translated_question['explanation'] = self.translate_text(question['explanation'], target_language)
                
                translated_questions.append(translated_question)
            
            return translated_questions
            
        except Exception as e:
            logger.error(f"Error translating quiz questions: {e}")
            return questions


# Global translator instance
translator = None

def get_translator():
    """Get or create translator instance"""
    global translator
    if translator is None:
        translator = IndicTrans2Service()
    return translator

def translate_to_language(text, language):
    """Quick translation function"""
    translator = get_translator()
    return translator.translate_text(text, language)

def translate_vocabulary_data():
    """Translate existing vocabulary data for all languages"""
    from mongodb_models import get_database
    
    # Sample vocabulary structure - replace with your actual data
    vocabulary_data = {
        'animals': {
            'dog': {'english': 'Dog'},
            'cat': {'english': 'Cat'},
            'cow': {'english': 'Cow'},
            'horse': {'english': 'Horse'},
            'goat': {'english': 'Goat'},
            'lion': {'english': 'Lion'},
            'elephant': {'english': 'Elephant'},
            'bear': {'english': 'Bear'},
            'monkey': {'english': 'Monkey'},
            'fox': {'english': 'Fox'}
        },
        'fruits': {
            'apple': {'english': 'Apple'},
            'banana': {'english': 'Banana'},
            'mango': {'english': 'Mango'},
            'orange': {'english': 'Orange'},
            'grapes': {'english': 'Grapes'},
            'strawberry': {'english': 'Strawberry'},
            'pineapple': {'english': 'Pineapple'},
            'watermelon': {'english': 'Watermelon'}
        },
        'colors': {
            'red': {'english': 'Red'},
            'blue': {'english': 'Blue'},
            'green': {'english': 'Green'},
            'yellow': {'english': 'Yellow'},
            'orange': {'english': 'Orange'},
            'purple': {'english': 'Purple'},
            'pink': {'english': 'Pink'},
            'black': {'english': 'Black'},
            'white': {'english': 'White'},
            'brown': {'english': 'Brown'}
        }
    }
    
    translator = get_translator()
    translated_vocab = translator.translate_vocabulary(vocabulary_data)
    
    # Store in database
    try:
        db = get_database()
        collection = db.multilingual_vocabulary
        
        # Clear existing data
        collection.delete_many({})
        
        # Insert translated vocabulary
        for category, items in translated_vocab.items():
            for item_key, item_data in items.items():
                document = {
                    'category': category,
                    'key': item_key,
                    'english': item_data['english'],
                    'translations': item_data['translations']
                }
                collection.insert_one(document)
        
        logger.info("Vocabulary translations stored in database successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to store translations in database: {e}")
        return False

if __name__ == "__main__":
    # Test the translation service
    translator = IndicTrans2Service()
    
    # Test single translation
    test_text = "Hello, how are you?"
    hindi_translation = translator.translate_text(test_text, "hindi")
    print(f"English: {test_text}")
    print(f"Hindi: {hindi_translation}")
    
    # Test batch translation
    test_texts = ["Dog", "Cat", "Elephant"]
    tamil_translations = translator.translate_batch(test_texts, "tamil")
    for eng, tam in zip(test_texts, tamil_translations):
        print(f"English: {eng} -> Tamil: {tam}")