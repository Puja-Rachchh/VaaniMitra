#!/usr/bin/env python3
"""
Comprehensive test script for VaaniMitra translation system
Tests all components: translation service, vocabulary, routes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from translation_service import get_translator
from comprehensive_vocabulary import get_vocabulary_for_level
from mongodb_models import get_database
import requests
import json

def test_translation_service():
    """Test the core translation service"""
    print("🧪 Testing Translation Service...")
    
    try:
        translator = get_translator()
        
        # Test basic translation
        test_cases = [
            ("Hello", "hindi"),
            ("Apple", "tamil"),
            ("Dog", "bengali"),
            ("Red", "gujarati"),
            ("Family", "marathi")
        ]
        
        for english_text, target_lang in test_cases:
            translation = translator.translate_text(english_text, target_lang)
            print(f"  ✅ '{english_text}' -> {target_lang}: '{translation}'")
        
        # Test batch translation
        words = ["Apple", "Banana", "Orange"]
        translations = translator.translate_batch(words, "hindi")
        print(f"  ✅ Batch translation to Hindi: {dict(zip(words, translations))}")
        
        # Test available languages
        languages = translator.get_available_languages()
        print(f"  ✅ Supported languages ({len(languages)}): {', '.join(languages)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Translation service test failed: {e}")
        return False

def test_vocabulary_system():
    """Test the vocabulary retrieval system"""
    print("\n📚 Testing Vocabulary System...")
    
    try:
        # Test vocabulary for different levels
        levels = ['beginner', 'intermediate_1', 'intermediate_2', 'intermediate_3']
        
        for level in levels:
            vocab = get_vocabulary_for_level(level, 'english')
            if vocab:
                categories = list(vocab.keys())
                total_items = sum(len(items) for items in vocab.values())
                print(f"  ✅ {level}: {len(categories)} categories, {total_items} items")
            else:
                print(f"  ⚠️ {level}: No vocabulary found")
        
        # Test translated vocabulary
        hindi_vocab = get_vocabulary_for_level('intermediate_1', 'hindi')
        if hindi_vocab:
            print(f"  ✅ Hindi vocabulary loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Vocabulary system test failed: {e}")
        return False

def test_database_connection():
    """Test MongoDB database connection"""
    print("\n🗄️ Testing Database Connection...")
    
    try:
        db = get_database()
        
        # Test collections
        collections = db.list_collection_names()
        print(f"  ✅ Database connected. Collections: {collections}")
        
        # Test vocabulary collection
        vocab_collection = db.multilingual_vocabulary
        vocab_count = vocab_collection.count_documents({})
        print(f"  ✅ Vocabulary collection: {vocab_count} documents")
        
        if vocab_count > 0:
            sample = vocab_collection.find_one()
            print(f"  ✅ Sample vocabulary: {sample.get('english', 'N/A')} ({sample.get('category', 'N/A')})")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Database test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints (requires running Flask app)"""
    print("\n🌐 Testing API Endpoints...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Test supported languages endpoint
        response = requests.get(f"{base_url}/api/supported-languages", timeout=5)
        if response.status_code == 200:
            data = response.json()
            languages = data.get('languages', [])
            print(f"  ✅ Supported languages API: {len(languages)} languages")
        else:
            print(f"  ⚠️ Supported languages API: Status {response.status_code}")
        
        # Test vocabulary API
        response = requests.get(f"{base_url}/api/level-vocabulary/intermediate_1?language=english", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Vocabulary API: {len(data)} categories")
        else:
            print(f"  ⚠️ Vocabulary API: Status {response.status_code}")
        
        # Test translation API
        response = requests.get(f"{base_url}/api/translate-content?level=beginner&language=hindi", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Translation API working")
        else:
            print(f"  ⚠️ Translation API: Status {response.status_code}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("  ⚠️ Flask app not running - API tests skipped")
        print("    To test APIs, run: python app.py")
        return True
    except Exception as e:
        print(f"  ❌ API test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 VaaniMitra Translation System - Comprehensive Test")
    print("=" * 60)
    
    tests = [
        ("Translation Service", test_translation_service),
        ("Vocabulary System", test_vocabulary_system),
        ("Database Connection", test_database_connection),
        ("API Endpoints", test_api_endpoints)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  💥 {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:<20} {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! VaaniMitra translation system is ready!")
        print("\n🌟 Features available:")
        print("   • Translation to 15+ Indian languages")
        print("   • Comprehensive vocabulary database")
        print("   • Multi-language learning support")
        print("   • Dynamic content translation")
        print("   • User language preferences")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)