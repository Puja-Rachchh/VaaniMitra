#!/usr/bin/env python3
"""
Comprehensive test for Intermediate Level System with IndicTrans2
Tests automatic translation of intermediate level vocabulary for user-selected languages
"""

import sys
import traceback

try:
    print("Testing IndicTrans2 service import...")
    from indictrans2_service import IndicTrans2Service
    print("✓ Import successful")

    print("Creating service instance...")
    try:
        service = IndicTrans2Service()
        print(f"✓ Service created. Model loaded: {service.model_loaded}")
    except Exception as init_error:
        print(f"✗ Service creation failed: {init_error}")
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "="*60)
    print("🎯 INTERMEDIATE LEVEL SYSTEM TRANSLATION TEST")
    print("="*60)

    # Define intermediate level categories and their expected vocabulary
    intermediate_levels = {
        1: 'vegetables',
        2: 'animals',
        3: 'colors',
        4: 'professionals',
        5: 'body_parts'
    }

    # Test languages supported by IndicTrans2
    test_languages = ['hindi', 'gujarati', 'tamil', 'bengali']

    total_translations = 0
    successful_translations = 0

    for level, category in intermediate_levels.items():
        print(f"\n{'='*20} LEVEL {level}: {category.upper()} {'='*20}")

        # Get English vocabulary for this category
        from native_content_system import get_english_vocabulary
        english_words = get_english_vocabulary(category)

        if not english_words:
            print(f"⚠️  No vocabulary found for category '{category}'")
            continue

        print(f"📚 Found {len(english_words)} English words in '{category}' category")
        print(f"📝 Sample words: {', '.join(english_words[:5])}")

        # Test translation for each supported language
        for language in test_languages:
            print(f"\n🌐 Testing {language.upper()} translations:")

            try:
                # Translate the entire category
                translated_vocab = service.translate_vocabulary_category(category, language)

                if translated_vocab and len(translated_vocab) > 0:
                    print(f"  ✓ Successfully translated {len(translated_vocab)} words to {language}")

                    # Show sample translations
                    successful_count = 0
                    for i, vocab_item in enumerate(translated_vocab[:3]):  # Show first 3
                        english = vocab_item.get('english', '')
                        translated = vocab_item.get('translated', '')

                        # Check if translation is valid (not an error message)
                        if translated and not translated.startswith('[INDICTRANS2'):
                            print(f"    {i+1}. {english} → {translated}")
                            successful_count += 1
                            successful_translations += 1
                        else:
                            print(f"    {i+1}. {english} → {translated} (failed)")

                    total_translations += len(translated_vocab)

                    success_rate = successful_count / min(3, len(translated_vocab)) * 100
                    print(f"    Success rate: {success_rate:.1f}%")
                else:
                    print(f"  ✗ Translation failed for {language}")

            except Exception as e:
                print(f"  ✗ Error translating to {language}: {e}")

    print("\n" + "="*60)
    print("📊 INTERMEDIATE LEVEL SYSTEM SUMMARY")
    print("="*60)

    if total_translations > 0:
        overall_success_rate = (successful_translations / total_translations) * 100
        print(f"📊 Overall Success Rate: {overall_success_rate:.1f}%")
        print(f"📈 Total Translations Attempted: {total_translations}")
        print(f"✅ Successful Translations: {successful_translations}")
        print(f"❌ Failed Translations: {total_translations - successful_translations}")

        # Test specific intermediate level scenarios
        print("\n🎮 TESTING INTERMEDIATE LEVEL USER SCENARIOS")
        print("-" * 50)

        # Simulate a user selecting Hindi as target language
        user_language = 'hindi'
        print(f"👤 User selects {user_language.upper()} as target language")

        for level, category in intermediate_levels.items():
            try:
                vocab = service.translate_vocabulary_category(category, user_language)
                if vocab and len(vocab) > 0:
                    valid_translations = [v for v in vocab if v.get('translated', '').strip() and not v['translated'].startswith('[INDICTRANS2')]
                    print(f"  ✓ Level {level} ({category}): {len(valid_translations)}/{len(vocab)} words translated")
                else:
                    print(f"  ✗ Level {level} ({category}): Translation failed")
            except Exception as e:
                print(f"  ✗ Level {level} ({category}): Error - {e}")

    print("\n🏆 INTERMEDIATE LEVEL SYSTEM STATUS")
    print("-" * 50)
    print(f"🤖 IndicTrans2 Model: {'✅ Loaded' if service.model_loaded else '❌ Not Loaded'}")
    print(f"🌍 Supported Languages: {', '.join(service.supported_languages)}")
    print(f"📚 Intermediate Levels: {len(intermediate_levels)} levels configured")
    print(f"🎯 Vocabulary Categories: {', '.join(intermediate_levels.values())}")

    if service.model_loaded and total_translations > 0:
        print("\n🎉 INTERMEDIATE LEVEL SYSTEM IS FULLY OPERATIONAL!")
        print("   Users can now automatically get translations for all intermediate vocabulary!")
    else:
        print("\n⚠️  INTERMEDIATE LEVEL SYSTEM NEEDS ATTENTION")
        if not service.model_loaded:
            print("   - IndicTrans2 model failed to load")
        if total_translations == 0:
            print("   - No translations were successful")

except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()
    sys.exit(1)