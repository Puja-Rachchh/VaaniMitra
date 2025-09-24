"""
IndicTrans2 Translation Service
Provides automatic translation from English to Indian languages using IndicTrans2 model
Uses native_content_system.py for English vocabulary categories
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from mongodb_models import mongo
from native_content_system import get_english_vocabulary, get_all_vocabulary_categories
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class IndicTrans2Service:
    def __init__(self):
        """Initialize IndicTrans2 model for translation"""
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.device = torch.device('cpu')  # Use CPU to avoid memory issues
        
        # Fallback translations for languages where IndicTrans2 has issues
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
                # Fruits
                'apple': 'ஆப்பிள்',
                'banana': 'வாழைப்பழம்',
                'mango': 'மாம்பழம்',
                'orange': 'ஆரஞ்சு',
                'grapes': 'திராட்சை',
                'watermelon': 'தர்பூசணி',
                'pineapple': 'அன்னாசிப்பழம்',
                'papaya': 'பப்பாளி',
                'pomegranate': 'மாதுளை',
                'strawberry': 'ஸ்ட்ராபெரி',
                'cherry': 'செர்ரி',
                'pear': 'பேரிக்காய்',
                'kiwi': 'கிவி',
                'lichi': 'லிச்சி',
                'sugarcane': 'கரும்பு',
                # Animals
                'dog': 'நாய்',
                'cat': 'பூனை',
                'cow': 'பசு',
                'horse': 'குதிரை',
                'lion': 'சிங்கம்',
                'tiger': 'புலி',
                'elephant': 'யானை',
                'monkey': 'கபி',
                'bear': 'கரடி',
                'fox': 'நரி',
                'rabbit': 'முயல்',
                'deer': 'மான்',
                'goat': 'ஆடு',
                'sheep': 'செம்மறி',
                'pig': 'பன்றி',
                'duck': 'வாத்து',
                'chicken': 'கோழி',
                'peacock': 'தோகை',
                'parrot': 'கிளி',
                'eagle': 'கழுகு',
                'snake': 'பாம்பு',
                'frog': 'தவழ்',
                'fish': 'மீன்',
                'butterfly': 'வண்ணத்துப்பூச்சி',
                'ant': 'எறும்பு',
                'bee': 'தேனீ'
            }
        }
        
        # Language mapping from app language names to IndicTrans2 codes
        self.language_mapping = {
            'hindi': 'hin_Deva',
            'gujarati': 'guj_Gujr', 
            'tamil': 'tam_Taml',
            'bengali': 'ben_Beng',
            'telugu': 'tel_Telu',
            'marathi': 'mar_Deva',
            'punjabi': 'pan_Guru',
            'urdu': 'urd_Arab',
            'kannada': 'kan_Knda',
            'malayalam': 'mal_Mlym',
            'odia': 'ory_Orya',
            'assamese': 'asm_Beng',
            'nepali': 'npi_Deva'
        }
        
        self.supported_languages = list(self.language_mapping.keys())
        
        # Try to load model once on startup (non-blocking)
        logger.info("Starting IndicTrans2 service initialization...")
        self._initialize_model()
        
    def check_model_availability(self):
        """Check if the IndicTrans2 model is available and working"""
        if self.model_loaded:
            try:
                # Test translation
                test_result = self.translate_text("hello", "hindi")
                logger.info(f"Model test successful: hello -> {test_result}")
                return True
            except Exception as e:
                logger.error(f"Model test failed: {e}")
                return False
        else:
            logger.warning("Model not loaded")
            return False
        
    def _initialize_model(self):
        """Initialize translation model - try multiple approaches"""
        try:
            logger.info("Trying multiple approaches to initialize IndicTrans2...")

            # Approach 1: Try direct model loading (simpler)
            try:
                logger.info("Approach 1: Direct model loading...")
                from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

                self.tokenizer = AutoTokenizer.from_pretrained(
                    "ai4bharat/indictrans2-en-indic-dist-200M",
                    trust_remote_code=True,
                    cache_dir="E:/VaaniMitraData/models"
                )

                self.model = AutoModelForSeq2SeqLM.from_pretrained(
                    "ai4bharat/indictrans2-en-indic-dist-200M",
                    trust_remote_code=True,
                    torch_dtype=torch.float32,
                    cache_dir="E:/VaaniMitraData/models"
                )

                self.model = self.model.to('cpu')
                self.device = torch.device('cpu')
                self.model.eval()

                # Debug: Check tokenizer and model properties
                logger.info("=== MODEL DEBUG INFO ===")
                logger.info(f"Tokenizer type: {type(self.tokenizer)}")
                logger.info(f"Model type: {type(self.model)}")
                logger.info(f"Tokenizer vocab size: {self.tokenizer.vocab_size}")
                logger.info(f"Model config: {self.model.config}")
                logger.info(f"Pad token: {self.tokenizer.pad_token}")
                logger.info(f"Pad token ID: {self.tokenizer.pad_token_id}")
                logger.info(f"EOS token: {self.tokenizer.eos_token}")
                logger.info(f"EOS token ID: {self.tokenizer.eos_token_id}")
                logger.info(f"BOS token: {self.tokenizer.bos_token}")
                logger.info(f"BOS token ID: {self.tokenizer.bos_token_id}")
                logger.info("=== END MODEL DEBUG ===")

                logger.info("Approach 1 successful!")
                self.model_loaded = True
                return

            except Exception as e1:
                logger.warning(f"Approach 1 failed: {e1}")

                # Approach 2: Try pipeline
                try:
                    logger.info("Approach 2: Pipeline approach...")
                    from transformers import pipeline

                    self.translator = pipeline(
                        "translation",
                        model="ai4bharat/indictrans2-en-indic-dist-200M",
                        device=-1,
                        trust_remote_code=True,
                        cache_dir="E:/VaaniMitraData/models"
                    )

                    logger.info("Approach 2 successful!")
                    self.model_loaded = True
                    return

                except Exception as e2:
                    logger.warning(f"Approach 2 failed: {e2}")

                    # Approach 3: Try alternative model
                    try:
                        logger.info("Approach 3: Alternative IndicTrans2 model...")
                        from transformers import pipeline

                        # Try the larger model
                        self.translator = pipeline(
                            "translation",
                            model="ai4bharat/indictrans2-en-indic-1B",
                            device=-1,
                            trust_remote_code=True,
                            cache_dir="E:/VaaniMitraData/models"
                        )

                        logger.info("Approach 3 successful!")
                        self.model_loaded = True
                        return

                    except Exception as e3:
                        logger.error(f"All approaches failed. Last error: {e3}")
                        self.model_loaded = False

        except Exception as e:
            logger.error(f"Critical error initializing translation model: {str(e)}")
            self.model_loaded = False

    def translate_text(self, text, target_language):
        """Translate English text to target Indian language using IndicTrans2 with fallback"""
        try:
            if not self.model_loaded:
                logger.error("IndicTrans2 model not loaded")
                # Try fallback even if model is not loaded
                fallback_result = self._get_fallback_translation(text, target_language)
                if fallback_result:
                    return fallback_result
                return f"[INDICTRANS2_UNAVAILABLE] {text}"

            # Check if we have pipeline or direct model
            logger.info(f"Checking translation methods: translator={hasattr(self, 'translator')}, model={hasattr(self, 'model')}")
            if hasattr(self, 'translator') and self.translator:
                logger.info("Using pipeline approach")
                result = self._translate_with_pipeline(text, target_language)
            elif hasattr(self, 'model') and self.model:
                logger.info("Using direct model approach")
                result = self._translate_with_model(text, target_language)
            else:
                logger.error("No translation method available")
                result = f"[INDICTRANS2_NO_METHOD] {text}"

            # Check if the result is valid (not an error and not in wrong script)
            if result and not result.startswith('[') and self._is_valid_translation(result, target_language):
                # Memory cleanup
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                return result
            else:
                # Try fallback translation
                logger.info(f"IndicTrans2 result invalid, trying fallback for '{text}' to {target_language}")
                fallback_result = self._get_fallback_translation(text, target_language)
                if fallback_result:
                    logger.info(f"Using fallback translation: '{fallback_result}'")
                    return fallback_result
                
                # Memory cleanup
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                return result

        except Exception as e:
            logger.error(f"Translation system error for '{text}': {e}")
            # Try fallback even on error
            fallback_result = self._get_fallback_translation(text, target_language)
            if fallback_result:
                return fallback_result
            return f"[INDICTRANS2_SYSTEM_ERROR] {text}"

    def _is_valid_translation(self, translation, target_language):
        """Check if the translation is in the correct script for the target language"""
        if not translation:
            return False
            
        # Check for wrong script issues
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
            
        elif target_language.lower() == 'gujarati':
            # Gujarati should contain Gujarati script characters (U+0A80-U+0AFF)
            has_gujarati = any('\u0a80' <= char <= '\u0aff' for char in translation)
            has_devanagari = any('\u0900' <= char <= '\u097f' for char in translation)
            
            # For Gujarati, prefer Gujarati script over Devanagari
            if has_devanagari and not has_gujarati:
                logger.warning(f"Invalid Gujarati translation '{translation}' - contains only Devanagari")
                return False
            return True
            
        elif target_language.lower() == 'bengali':
            # Bengali should contain Bengali script characters (U+0980-U+09FF)
            has_bengali = any('\u0980' <= char <= '\u09ff' for char in translation)
            has_devanagari = any('\u0900' <= char <= '\u097f' for char in translation)
            
            if has_devanagari and not has_bengali:
                logger.warning(f"Invalid Bengali translation '{translation}' - contains only Devanagari")
                return False
            return True
            
        # Add more language validations as needed
        
        return True  # Default to valid for other languages

    def _get_fallback_translation(self, text, target_language):
        """Get fallback translation from manual mapping"""
        if target_language in self.fallback_translations:
            return self.fallback_translations[target_language].get(text.lower())
        return None

    def _translate_with_pipeline(self, text, target_language):
        """Translate using pipeline approach with proper IndicTrans2 preprocessing"""
        # Map language names to IndicTrans2 codes
        lang_map = {
            'gujarati': 'guj_Gujr',
            'hindi': 'hin_Deva',
            'bengali': 'ben_Beng',
            'tamil': 'tam_Taml',
            'telugu': 'tel_Telu',
            'marathi': 'mar_Deva',
            'kannada': 'kan_Knda',
            'malayalam': 'mal_Mlym',
            'punjabi': 'pan_Guru',
            'odia': 'ory_Orya'
        }

        target_code = lang_map.get(target_language.lower())
        if not target_code:
            logger.warning(f"Language {target_language} not supported by IndicTrans2")
            return f"[UNSUPPORTED_LANGUAGE_{target_language.upper()}] {text}"

        try:
            # Use the pipeline with proper parameters from HuggingFace documentation
            result = self.translator(
                text, 
                src_lang="eng_Latn", 
                tgt_lang=target_code,
                num_beams=5,  # Official parameter from documentation
                max_length=256,  # Official parameter from documentation
                min_length=0,  # Official parameter from documentation
                do_sample=False,
                use_cache=False  # Disable caching to avoid past_key_values issues
            )

            if result and len(result) > 0:
                translation = result[0].get('translation_text', '').strip()

                # Apply manual postprocessing
                processed_translations = self._postprocess_batch([translation], tgt_lang=target_code)
                translation = processed_translations[0]

                if translation and translation != text:
                    logger.info(f"IndicTrans2 pipeline translated '{text}' to '{translation}'")
                    return translation
                else:
                    logger.warning(f"IndicTrans2 pipeline returned empty/same result for '{text}'")
                    return f"[INDICTRANS2_NO_RESULT] {text}"
            else:
                logger.warning(f"IndicTrans2 pipeline returned no result for '{text}'")
                return f"[INDICTRANS2_NO_RESULT] {text}"

        except Exception as pipeline_error:
            logger.error(f"IndicTrans2 pipeline failed for '{text}': {pipeline_error}")
            return f"[INDICTRANS2_PIPELINE_ERROR] {text}"

    def _translate_with_model(self, text, target_language):
        """Translate using direct model approach with proper IndicTrans2 preprocessing"""
        # Map language names to IndicTrans2 codes
        lang_map = {
            'gujarati': 'guj_Gujr',
            'hindi': 'hin_Deva',
            'bengali': 'ben_Beng',
            'tamil': 'tam_Taml',
            'telugu': 'tel_Telu',
            'marathi': 'mar_Deva',
            'kannada': 'kan_Knda',
            'malayalam': 'mal_Mlym',
            'punjabi': 'pan_Guru',
            'odia': 'ory_Orya'
        }

        target_code = lang_map.get(target_language.lower())
        if not target_code:
            logger.warning(f"Language {target_language} not supported by IndicTrans2")
            return f"[UNSUPPORTED_LANGUAGE_{target_language.upper()}] {text}"

        try:
            # Preprocess the input text (manual implementation)
            logger.info(f"Preprocessing text: '{text}' for target language: {target_language}")
            processed_texts = self._preprocess_batch([text], src_lang="eng_Latn", tgt_lang=target_code)
            input_text = processed_texts[0]
            logger.info(f"Preprocessed text: '{input_text}'")

            # Tokenize with proper parameters
            logger.info("Starting tokenization...")
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=256  # Increased from 128 to match documentation
            )
            logger.info(f"Tokenization successful. Input IDs shape: {inputs['input_ids'].shape}")
            logger.info(f"Input IDs: {inputs['input_ids']}")
            logger.info(f"Attention mask: {inputs.get('attention_mask', 'None')}")

            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            logger.info(f"Moved inputs to device: {self.device}")

            # Generate with official IndicTrans2 parameters from HuggingFace documentation
            logger.info("Starting model generation...")
            with torch.no_grad():
                try:
                    logger.info("Calling model.generate() with parameters:")
                    logger.info(f"  num_beams: 5")
                    logger.info(f"  max_length: 256")
                    logger.info(f"  min_length: 0")
                    logger.info(f"  pad_token_id: {self.tokenizer.pad_token_id}")
                    logger.info(f"  eos_token_id: {self.tokenizer.eos_token_id}")
                    logger.info(f"  bos_token_id: {self.tokenizer.bos_token_id}")

                    outputs = self.model.generate(
                        inputs['input_ids'],
                        attention_mask=inputs.get('attention_mask'),
                        num_beams=5,  # Official parameter from documentation
                        max_length=256,  # Official parameter from documentation
                        min_length=0,  # Official parameter from documentation
                        do_sample=False,
                        use_cache=False,  # Disable caching to avoid past_key_values issues
                        pad_token_id=self.tokenizer.pad_token_id,
                        eos_token_id=self.tokenizer.eos_token_id,
                        bos_token_id=self.tokenizer.bos_token_id
                    )

                    logger.info(f"Generation successful. Output shape: {outputs.shape}")
                    logger.info(f"Output tokens: {outputs[0]}")

                    # Decode the generated tokens
                    raw_translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                    logger.info(f"Raw decoded translation: '{raw_translation}'")

                    # Postprocess the translation (manual implementation)
                    processed_translations = self._postprocess_batch([raw_translation], tgt_lang=target_code)
                    translation = processed_translations[0]
                    logger.info(f"Postprocessed translation: '{translation}'")

                    # Final cleanup
                    translation = translation.strip()

                    if translation and translation != text:
                        logger.info(f"IndicTrans2 model translated '{text}' to '{translation}'")
                        return translation
                    else:
                        logger.warning(f"IndicTrans2 model returned empty/same result for '{text}'")
                        return f"[INDICTRANS2_NO_RESULT] {text}"

                except Exception as inner_error:
                    logger.error(f"Inner generation error details: {inner_error}")
                    logger.error(f"Error type: {type(inner_error)}")
                    import traceback
                    logger.error(f"Full traceback: {traceback.format_exc()}")
                    raise inner_error

        except Exception as gen_error:
            logger.error(f"IndicTrans2 model generation failed for '{text}': {gen_error}")
            logger.error(f"Error type: {type(gen_error)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return f"[INDICTRANS2_GENERATION_ERROR] {text}"

    def _preprocess_batch(self, texts, src_lang="eng_Latn", tgt_lang="tam_Taml"):
        """
        Manual preprocessing for IndicTrans2 based on HuggingFace documentation
        The tokenizer expects format: 'src_lang tgt_lang text'
        """
        processed_texts = []
        
        for text in texts:
            # Use the correct format that IndicTrans2 tokenizer expects
            # Format: src_lang tgt_lang text (e.g., "eng_Latn hin_Deva hello")
            processed_text = f"{src_lang} {tgt_lang} {text}"
            processed_texts.append(processed_text)
        
        return processed_texts
    
    def _postprocess_batch(self, translations, tgt_lang):
        """
        Manual postprocessing for IndicTrans2 based on HuggingFace documentation
        Since we're using the correct tokenizer format, minimal postprocessing is needed
        """
        processed_translations = []
        
        for translation in translations:
            # The tokenizer handles language tags internally, so just clean up
            if isinstance(translation, str):
                # Remove any remaining special tokens if present
                translation = translation.replace("<pad>", "").replace("</s>", "").strip()
                processed_translations.append(translation)
            else:
                processed_translations.append(str(translation))
        
        return processed_translations

    def translate_vocabulary_category(self, category, target_language):
        """
        Translate an entire vocabulary category from English to target language
        Uses native_content_system.py for English vocabulary
        """
        try:
            # Get English words for this category from native_content_system
            english_words = get_english_vocabulary(category)
            if not english_words:
                logger.warning(f"No vocabulary found for category '{category}'")
                return []
            
            logger.info(f"Translating {len(english_words)} words from '{category}' category to {target_language}")
            
            # Check cache first
            cached_vocabulary = self._get_cached_vocabulary(category, target_language)
            if cached_vocabulary:
                logger.info(f"Found cached vocabulary for {category} in {target_language}")
                return cached_vocabulary
            
            # Translate each word using IndicTrans2 model only
            translated_vocabulary = []
            successful_translations = 0
            failed_translations = 0
            
            for i, english_word in enumerate(english_words):
                try:
                    logger.info(f"Translating word {i+1}/{len(english_words)}: '{english_word}'")
                    translated_word = self.translate_text(english_word, target_language)
                    
                    # Check if translation is valid (not an error message)
                    if translated_word and not translated_word.startswith('[') and translated_word != english_word:
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
                    
                    # Add small delay and memory cleanup between translations
                    import time
                    time.sleep(0.1)  # Small delay to prevent memory buildup
                    
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
            
            # Cache the results if we have translations
            if translated_vocabulary:
                self._cache_vocabulary(category, target_language, translated_vocabulary)
            
            logger.info(f"Successfully translated {len(translated_vocabulary)} words for category '{category}'")
            return translated_vocabulary
            
        except Exception as e:
            logger.error(f"Error translating vocabulary category '{category}' to {target_language}: {str(e)}")
            # Return English words as fallback
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
        """
        Translate an entire vocabulary category from English to target language
        Uses native_content_system.py for English vocabulary
        """
        try:
            # Get English words for this category from native_content_system
            english_words = get_english_vocabulary(category)
            if not english_words:
                logger.warning(f"No vocabulary found for category '{category}'")
                return []
            
            logger.info(f"Translating {len(english_words)} words from '{category}' category to {target_language}")
            
            # Check cache first
            cached_vocabulary = self._get_cached_vocabulary(category, target_language)
            if cached_vocabulary:
                logger.info(f"Found cached vocabulary for {category} in {target_language}")
                return cached_vocabulary
            
            # Translate each word (with fallback support)
            translated_vocabulary = []
            for english_word in english_words:
                try:
                    translated_word = self.translate_text(english_word, target_language)
                    
                    vocab_item = {
                        'english': english_word,
                        'translated': translated_word,
                        'category': category,
                        'target_language': target_language
                    }
                    translated_vocabulary.append(vocab_item)
                    
                except Exception as e:
                    logger.error(f"Error translating '{english_word}': {str(e)}")
                    # Add untranslated word as fallback
                    vocab_item = {
                        'english': english_word,
                        'translated': english_word,  # Fallback to English
                        'category': category,
                        'target_language': target_language
                    }
                    translated_vocabulary.append(vocab_item)
            
            # Cache the results if we have translations
            if translated_vocabulary:
                self._cache_vocabulary(category, target_language, translated_vocabulary)
            
            logger.info(f"Successfully translated {len(translated_vocabulary)} words for category '{category}'")
            return translated_vocabulary
            
        except Exception as e:
            logger.error(f"Error translating vocabulary category '{category}' to {target_language}: {str(e)}")
            # Return English words as fallback
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
    
    def _get_cached_vocabulary(self, category, target_language):
        """Get cached vocabulary from MongoDB"""
        try:
            cached_vocab = mongo.db.multilingual_vocabulary.find_one({
                'category': category,
                'target_language': target_language
            })
            
            if cached_vocab and cached_vocab.get('vocabulary'):
                return cached_vocab['vocabulary']
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving cached vocabulary: {str(e)}")
            return None
    
    def _cache_vocabulary(self, category, target_language, vocabulary):
        """Cache vocabulary in MongoDB"""
        try:
            # Check if entry exists
            existing = mongo.db.multilingual_vocabulary.find_one({
                'category': category,
                'target_language': target_language
            })
            
            vocab_data = {
                'category': category,
                'target_language': target_language,
                'vocabulary': vocabulary,
                'last_updated': datetime.utcnow()
            }
            
            if existing:
                # Update existing entry
                mongo.db.multilingual_vocabulary.update_one(
                    {'_id': existing['_id']},
                    {'$set': vocab_data}
                )
            else:
                # Create new entry
                vocab_data['created_at'] = datetime.utcnow()
                mongo.db.multilingual_vocabulary.insert_one(vocab_data)
            
            logger.info(f"Cached vocabulary for {category} in {target_language}")
            
        except Exception as e:
            logger.error(f"Error caching vocabulary: {str(e)}")
    
    def get_all_available_categories(self):
        """Get all vocabulary categories available from native_content_system"""
        return get_all_vocabulary_categories()
    
    def batch_translate(self, texts, target_language):
        """Translate multiple texts at once for better efficiency"""
        try:
            if not self.model_loaded:
                logger.warning("IndicTrans2 model not loaded, returning original texts")
                return texts
            
            # Get the target language code for IndicTrans2
            target_code = self.language_mapping.get(target_language.lower())
            if not target_code:
                logger.warning(f"Language {target_language} not supported, returning original texts")
                return texts
            
            # For now, translate individually to avoid batch errors
            translated_texts = []
            for text in texts:
                translated = self.translate_text(text, target_language)
                translated_texts.append(translated)
            
            logger.info(f"Batch translated {len(texts)} texts to {target_language}")
            return translated_texts
            
        except Exception as e:
            logger.error(f"Error in batch translation to {target_language}: {str(e)}")
            return texts

# Global service instance
translation_service = IndicTrans2Service()