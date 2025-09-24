#!/usr/bin/env python3
"""
Test script for IndicTrans2 automatic translation functionality
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_english_vocabulary():
    """Test English vocabulary retrieval"""
    print("Testing English vocabulary retrieval...")
    
    from native_content_system import get_english_vocabulary, get_all_vocabulary_categories
    
    categories = get_all_vocabulary_categories()
    print(f"Available categories: {categories}")
    
    fruits = get_english_vocabulary('fruits')
    print(f"English fruits ({len(fruits)} items): {fruits[:5]}...")
    
    animals = get_english_vocabulary('animals')
    print(f"English animals ({len(animals)} items): {animals[:5]}...")
    
    return True

def test_translation_service():
    """Test IndicTrans2 translation service"""
    print("\nTesting IndicTrans2 translation service...")
    
    try:
        from indictrans2_service import get_translation_service
        
        service = get_translation_service()
        print(f"Supported languages: {service.supported_languages}")
        
        # Test single translation
        print("\nTesting single word translation:")
        test_word = "apple"
        translation = service.translate_text(test_word, "gujarati")
        print(f"'{test_word}' in Gujarati: '{translation}'")
        
        # Test batch translation
        print("\nTesting batch translation:")
        test_words = ["apple", "banana", "mango"]
        translations = service.translate_batch(test_words, "hindi")
        for english, hindi in zip(test_words, translations):
            print(f"'{english}' in Hindi: '{hindi}'")
        
        return True
        
    except Exception as e:
        print(f"Translation service test failed: {e}")
        print("Note: This is expected if IndicTrans2 model is not downloaded yet.")
        return False

def test_vocabulary_category_translation():
    """Test full category translation with caching"""
    print("\nTesting vocabulary category translation...")
    
    try:
        from indictrans2_service import get_translation_service
        from native_content_system import get_english_vocabulary
        
        service = get_translation_service()
        
        # Get English fruits
        fruits = get_english_vocabulary('fruits')[:5]  # Test with first 5 fruits
        print(f"Testing with fruits: {fruits}")
        
        # Translate to Gujarati
        translated = service.translate_vocabulary_category('fruits', 'gujarati', fruits)
        print(f"Translated to Gujarati:")
        for english, gujarati in translated.items():
            print(f"  {english} -> {gujarati}")
        
        return True
        
    except Exception as e:
        print(f"Category translation test failed: {e}")
        return False

def test_mongodb_caching():
    """Test MongoDB caching functionality"""
    print("\nTesting MongoDB caching...")
    
    try:
        from app import app
        from mongodb_models import MultilingualVocabulary
        
        with app.app_context():
            # Try to find a cached item
            vocab_item = MultilingualVocabulary.find_by_key('fruits', 'apple')
            if vocab_item:
                print(f"Found cached translation for 'apple': {vocab_item.translations}")
            else:
                print("No cached translations found yet.")
                print("Translations will be cached when you first use the intermediate levels.")
        
        return True
        
    except Exception as e:
        print(f"MongoDB caching test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("VaaniMitra IndicTrans2 Translation System Test")
    print("=" * 60)
    
    tests = [
        ("English Vocabulary", test_english_vocabulary),
        ("Translation Service", test_translation_service),
        ("Category Translation", test_vocabulary_category_translation),
        ("MongoDB Caching", test_mongodb_caching)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"Test '{test_name}' failed with error: {e}")
            results.append((test_name, False))
    
    print(f"\n{'='*20} Test Results {'='*20}")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\n{'='*60}")
    print("Next steps:")
    print("1. Start the Flask app: python app.py")
    print("2. Login and select a target language")
    print("3. Go to intermediate levels to see automatic translation")
    print("4. Words will be translated and cached on first access")
    print("=" * 60)

if __name__ == "__main__":
    main()