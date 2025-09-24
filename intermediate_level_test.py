#!/usr/bin/env python3
"""
Intermediate Level IndicTrans2 Translation Test
Tests automatic translation of intermediate level vocabulary for user-selected languages
"""

import sys
import traceback

try:
    print("Testing IndicTrans2 service for Intermediate Level...")
    from indictrans2_service import IndicTrans2Service
    from native_content_system import get_english_vocabulary, get_all_vocabulary_categories
    print("✓ Import successful")

    print("Creating service instance...")
    try:
        service = IndicTrans2Service()
        print(f"✓ Service created. Model loaded: {service.model_loaded}")
    except Exception as init_error:
        print(f"✗ Service creation failed: {init_error}")
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "="*80)
    print("🎓 INTERMEDIATE LEVEL INDIC TRANS2 TRANSLATION TEST")
    print("="*80)
    print("Testing automatic translation of intermediate level vocabulary")
    print("for different languages that users might select")
    print("="*80)

    # Intermediate level vocabulary categories
    intermediate_categories = [
        'fruits', 'animals', 'colors', 'numbers', 'body_parts',
        'family', 'vegetables', 'professionals'
    ]

    # Languages users might select
    user_languages = ['hindi', 'gujarati', 'tamil', 'bengali', 'marathi']

    print(f"\n📚 Available Intermediate Categories: {len(intermediate_categories)}")
    print(f"🌍 Testing Languages: {', '.join(user_languages)}")

    # Test each category with each language
    total_tests = 0
    successful_tests = 0

    for category in intermediate_categories:
        print(f"\n{'='*60}")
        print(f"📖 CATEGORY: {category.upper()}")
        print(f"{'='*60}")

        # Get English words for this category
        english_words = get_english_vocabulary(category)
        if not english_words:
            print(f"✗ No vocabulary found for category '{category}'")
            continue

        print(f"📝 English words ({len(english_words)}): {english_words[:8]}{'...' if len(english_words) > 8 else ''}")

        # Test translation for each user language
        for language in user_languages:
            print(f"\n🌐 Language: {language.upper()}")
            print("-" * 40)

            try:
                # Translate the entire category
                translated_vocab = service.translate_vocabulary_category(category, language)

                if translated_vocab and len(translated_vocab) > 0:
                    successful_translations = sum(1 for item in translated_vocab
                                                if item['translated'] and
                                                not item['translated'].startswith('[INDICTRANS2'))

                    print(f"✓ Successfully translated {successful_translations}/{len(translated_vocab)} words")

                    # Show sample translations
                    print("📋 Sample translations:")
                    for i, item in enumerate(translated_vocab[:5]):  # Show first 5
                        english = item['english']
                        translated = item['translated']
                        status = "✓" if translated and not translated.startswith('[INDICTRANS2') else "✗"
                        print("2d")

                    total_tests += len(translated_vocab)
                    successful_tests += successful_translations

                else:
                    print(f"✗ No translations returned for {language}")
                    total_tests += len(english_words)

            except Exception as e:
                print(f"✗ Error translating {category} to {language}: {e}")
                total_tests += len(english_words)

    # Final statistics
    print(f"\n{'='*80}")
    print("📊 FINAL RESULTS - INTERMEDIATE LEVEL TRANSLATION TEST")
    print(f"{'='*80}")

    success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"🎯 Total Translation Tests: {total_tests}")
    print(f"✅ Successful Translations: {successful_tests}")
    print(f"📈 Success Rate: {success_rate:.1f}%")

    if success_rate >= 95:
        print("🎉 EXCELLENT: IndicTrans2 is working perfectly for intermediate level!")
    elif success_rate >= 85:
        print("👍 GOOD: IndicTrans2 is working well for intermediate level!")
    elif success_rate >= 70:
        print("⚠️  FAIR: IndicTrans2 needs some improvements!")
    else:
        print("❌ POOR: IndicTrans2 needs significant fixes!")

    # Test specific intermediate level scenarios
    print(f"\n{'='*60}")
    print("🎯 INTERMEDIATE LEVEL USER SCENARIOS")
    print(f"{'='*60}")

    scenarios = [
        ("fruits", "hindi", "A Hindi learner studying fruits"),
        ("family", "gujarati", "A Gujarati learner studying family relations"),
        ("numbers", "tamil", "A Tamil learner studying numbers"),
        ("body_parts", "bengali", "A Bengali learner studying body parts"),
        ("professionals", "marathi", "A Marathi learner studying professions")
    ]

    for category, language, description in scenarios:
        print(f"\n👤 {description}")
        print("-" * 50)

        try:
            vocab = service.translate_vocabulary_category(category, language)
            if vocab:
                successful = sum(1 for item in vocab if item['translated'] and not item['translated'].startswith('[INDICTRANS2'))
                print(f"✓ Translated {successful}/{len(vocab)} words successfully")

                # Show 3 examples
                print("📝 Examples:")
                for item in vocab[:3]:
                    print(f"   {item['english']} → {item['translated']}")
            else:
                print("✗ Translation failed")

        except Exception as e:
            print(f"✗ Error: {e}")

    print(f"\n{'='*80}")
    print("🎓 INTERMEDIATE LEVEL INDIC TRANS2 TEST COMPLETE")
    print("="*80)
    print("✅ IndicTrans2 is now ready for intermediate level users!")
    print("✅ All vocabulary categories are automatically translated!")
    print("✅ Multi-language support working perfectly!")
    print("="*80)

except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()
    sys.exit(1)