#!/usr/bin/env python3
"""
Test IndicTrans2 model output for words not in fallback
"""

from translation_service import IndicTrans2Service

def test_model_translations():
    service = IndicTrans2Service()
    
    # Test words not in fallback translations
    test_words = ['butterfly', 'computer', 'telephone', 'bicycle']
    test_languages = ['gujarati', 'tamil', 'bengali']
    
    print("Testing IndicTrans2 model translations (non-fallback words)...")
    print("=" * 70)
    
    for lang in test_languages:
        print(f"\n{lang.upper()} TRANSLATIONS:")
        print("-" * 30)
        
        for word in test_words:
            translation = service.translate_text(word, lang)
            print(f"{word:12} -> {translation}")
            
            # Check script validation
            if service._is_valid_translation(translation, lang):
                print(f"             ✓ Valid {lang} script")
            else:
                print(f"             ✗ Invalid {lang} script!")
        print()

if __name__ == "__main__":
    test_model_translations()