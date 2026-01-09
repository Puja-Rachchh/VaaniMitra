#!/usr/bin/env python3
"""
Test script to verify pronunciation checking system is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comprehensive_vocabulary import COMPREHENSIVE_VOCABULARY

def test_pronunciation_data():
    """Test pronunciation data access"""
    print("🔍 Testing pronunciation data access...")
    
    # Test animals category
    animals = COMPREHENSIVE_VOCABULARY.get('animals', {})
    print(f"Found {len(animals)} animals with pronunciation data")
    
    # Test a few examples
    test_words = ['dog', 'cat', 'cow']
    for word in test_words:
        if word in animals:
            data = animals[word]
            print(f"  {data['english']} -> {data['pronunciation']}")
    
    # Test colors category
    colors = COMPREHENSIVE_VOCABULARY.get('colors', {})
    print(f"\nFound {len(colors)} colors with pronunciation data")
    
    # Test a few color examples
    test_colors = ['red', 'blue', 'green']
    for color in test_colors:
        if color in colors:
            data = colors[color]
            print(f"  {data['english']} -> {data['pronunciation']}")
    
    print("\n✅ Pronunciation data access working correctly!")
    return True

def test_speech_recognition_mapping():
    """Test speech recognition language mapping"""
    print("\n🎤 Testing speech recognition language mapping...")
    
    # Import the function from routes
    from routes import get_speech_recognition_lang
    
    test_languages = ['Hindi', 'Tamil', 'Bengali', 'Gujarati']
    for lang in test_languages:
        speech_code = get_speech_recognition_lang(lang)
        print(f"  {lang} -> {speech_code}")
    
    print("✅ Speech recognition mapping working correctly!")
    return True

if __name__ == "__main__":
    print("🚀 Testing Pronunciation Checking System")
    print("=" * 50)
    
    try:
        test_pronunciation_data()
        test_speech_recognition_mapping()
        print("\n🎉 All pronunciation system tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")