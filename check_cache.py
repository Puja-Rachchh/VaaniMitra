from mongodb_models import mongo
from app import app

with app.app_context():
    # Check what Tamil translations are currently cached
    cached_items = list(mongo.db.multilingual_vocabulary.find({'target_language': 'tamil', 'category': 'colors'}))
    print(f'Found {len(cached_items)} cached Tamil color translations:')
    for item in cached_items:
        print(f"  {item['english']} -> {item['translated']}")
        # Check script
        translation = item['translated']
        has_tamil = any('\u0b80' <= char <= '\u0bff' for char in translation)
        has_devanagari = any('\u0900' <= char <= '\u097f' for char in translation)
        print(f"    Tamil script: {has_tamil}, Devanagari script: {has_devanagari}")