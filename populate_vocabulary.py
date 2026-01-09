#!/usr/bin/env python3
"""
Script to populate MongoDB with vocabulary data for faster retrieval
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from mongodb_models import MultilingualVocabulary, get_database, mongo
from comprehensive_vocabulary import COMPREHENSIVE_VOCABULARY
from translation_service import get_translator
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_vocabulary_to_mongodb():
    """Populate MongoDB with comprehensive vocabulary and translations for Hindi"""
    
    with app.app_context():
        try:
            logger.info("Starting vocabulary population to MongoDB...")
            
            # Get translator instance
            translator = get_translator()
            
            # Get database connection
            try:
                db = get_database()
                collection = db.multilingual_vocabulary
                logger.info("Database connection established")
            except Exception as db_error:
                logger.error(f"Database connection failed: {db_error}")
                # Try alternative connection method
                try:
                    db = mongo.db
                    collection = db.multilingual_vocabulary
                    logger.info("Alternative database connection established")
                except Exception as alt_error:
                    logger.error(f"Alternative database connection failed: {alt_error}")
                    return False
            
            # Clear existing data for fresh start
            try:
                result = collection.delete_many({})
                logger.info(f"Cleared {result.deleted_count} existing vocabulary items")
            except Exception as clear_error:
                logger.warning(f"Could not clear existing data: {clear_error}")
            
            total_items = 0
            target_language = 'hindi'  # Focus on Hindi first
            
            for category, items in COMPREHENSIVE_VOCABULARY.items():
                logger.info(f"Processing category: {category} with {len(items)} items")
                
                for key, data in items.items():
                    english_text = data['english']
                    
                    # For Hindi, we already have pronunciations in the data
                    hindi_translation = data.get('pronunciation', '')
                    
                    # If no pronunciation available, try translation
                    if not hindi_translation:
                        try:
                            hindi_translation = translator.translate_text(english_text, target_language)
                            logger.debug(f"Translated '{english_text}' to Hindi: '{hindi_translation}'")
                        except Exception as trans_error:
                            logger.warning(f"Failed to translate '{english_text}' to Hindi: {trans_error}")
                            hindi_translation = english_text  # Fallback
                    
                    # Create vocabulary item
                    vocab_item = {
                        'category': category,
                        'key': key,
                        'english': english_text,
                        'translations': {
                            'hindi': hindi_translation
                        },
                        'pronunciation': data.get('pronunciation', ''),
                        'description': data.get('description', ''),
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }
                    
                    try:
                        # Check if item already exists
                        existing = collection.find_one({
                            'category': category,
                            'key': key
                        })
                        
                        if existing:
                            # Update existing item
                            collection.update_one(
                                {'_id': existing['_id']},
                                {'$set': vocab_item}
                            )
                            logger.debug(f"Updated vocabulary item: {english_text}")
                        else:
                            # Insert new item
                            collection.insert_one(vocab_item)
                            logger.debug(f"Inserted vocabulary item: {english_text}")
                        
                        total_items += 1
                    except Exception as insert_error:
                        logger.warning(f"Failed to process {english_text}: {insert_error}")
            
            logger.info(f"✅ Successfully populated {total_items} vocabulary items with Hindi translations")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to populate vocabulary: {e}")
            return False

def test_vocabulary_retrieval():
    """Test vocabulary retrieval from MongoDB"""
    with app.app_context():
        try:
            logger.info("Testing vocabulary retrieval...")
            
            # Test categories for different levels
            test_categories = ['fruits', 'animals', 'colors', 'body_parts', 'family_relations']
            
            for category in test_categories:
                vocab_items = MultilingualVocabulary.get_vocabulary_by_category(category, 'hindi')
                logger.info(f"Category '{category}': Found {len(vocab_items)} items")
                
                # Show first 3 items as sample
                for i, item in enumerate(vocab_items[:3]):
                    logger.info(f"  {i+1}. {item['english']} -> {item['translation']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to test vocabulary retrieval: {e}")
            return False

if __name__ == "__main__":
    print("🚀 Starting vocabulary population for MongoDB...")
    
    # Populate vocabulary
    if populate_vocabulary_to_mongodb():
        print("✅ Vocabulary population completed successfully!")
        
        # Test retrieval
        print("\n🔍 Testing vocabulary retrieval...")
        if test_vocabulary_retrieval():
            print("✅ Vocabulary retrieval test successful!")
        else:
            print("❌ Vocabulary retrieval test failed!")
    else:
        print("❌ Vocabulary population failed!")