from translation_service import IndicTrans2Service
from app import app

with app.app_context():
    print("Testing updated translation_service.py...")
    
    # Create translation service instance
    service = IndicTrans2Service()
    
    # Test individual color translations
    test_colors = ['red', 'blue', 'green', 'yellow']
    
    for color in test_colors:
        result = service.translate_text(color, 'tamil')
        print(f"{color} -> {result}")
        
        # Check script
        if result and not result.startswith('['):
            has_tamil = any('\u0b80' <= char <= '\u0bff' for char in result)
            has_devanagari = any('\u0900' <= char <= '\u097f' for char in result)
            print(f"  Tamil script: {has_tamil}, Devanagari script: {has_devanagari}")
            if has_devanagari:
                print(f"  ERROR: Contains Devanagari characters!")
        print("---")
    
    print("\nTesting vocabulary category translation...")
    vocabulary_result = service.translate_vocabulary_category('colors', 'tamil')
    print(f"Got {len(vocabulary_result)} vocabulary items:")
    for item in vocabulary_result[:3]:  # First 3 items
        print(f"  {item['english']} -> {item['translated']}")
        translation = item['translated']
        if translation and not translation.startswith('['):
            has_tamil = any('\u0b80' <= char <= '\u0bff' for char in translation)
            has_devanagari = any('\u0900' <= char <= '\u097f' for char in translation)
            print(f"    Tamil script: {has_tamil}, Devanagari script: {has_devanagari}")
            if has_devanagari:
                print(f"    ERROR: Contains Devanagari characters!")