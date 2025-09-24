#!/usr/bin/env python3
"""
Test the intermediate level 2 route
"""

import sys
sys.path.append('.')

from native_content_system import get_english_vocabulary
from indictrans2_service import translation_service

# Simulate the route logic
category = 'animals'
target_language = 'gujarati'

print(f"Testing category: {category}, target_language: {target_language}")

# Get English vocabulary
english_words = get_english_vocabulary(category)
print(f"English words ({len(english_words)}): {english_words[:5]}...")

# Translate to target language
translated_vocab = translation_service.translate_vocabulary_category(
    category, target_language
)

print(f"Translated vocab ({len(translated_vocab)} items):")
for i, item in enumerate(translated_vocab[:5]):
    print(f"  {i+1}. {item.get('english', '')} -> {item.get('translated', '')}")

# Format vocabulary for template
vocabulary_items = []
for vocab_item in translated_vocab:
    vocabulary_items.append({
        'english': vocab_item.get('english', ''),
        'translation': vocab_item.get('translated', vocab_item.get('english', '')),
        'category': category
    })

print(f"\nVocabulary items for template ({len(vocabulary_items)}):")
for i, item in enumerate(vocabulary_items[:5]):
    print(f"  {i+1}. english='{item['english']}', translation='{item['translation']}'")

# Check for any error messages
error_count = 0
for item in vocabulary_items:
    if '[' in item['translation'] and ']' in item['translation']:
        print(f"Error in translation: {item['english']} -> {item['translation']}")
        error_count += 1

if error_count == 0:
    print("All translations look good!")
else:
    print(f"Found {error_count} error messages in translations")