#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from indictrans2_service import get_translation_service

def test_fallback_lookup():
    print("=== Testing Fallback Translation Lookup ===")
    
    service = get_translation_service()
    
    # Test individual fallback lookup
    print("Fallback translations structure:")
    print("Available categories:", list(service.fallback_translations.keys()))
    
    if 'vegetables' in service.fallback_translations:
        veg_dict = service.fallback_translations['vegetables']
        print("Vegetables in fallback:", list(veg_dict.keys())[:5])
        
        if 'potato' in veg_dict:
            potato_translations = veg_dict['potato']
            print("Potato translations:", potato_translations)
            print("Available languages for potato:", list(potato_translations.keys()))
    
    # Test the _get_fallback_translation method directly
    print("\nTesting _get_fallback_translation method:")
    result1 = service._get_fallback_translation('potato', 'gujarati')
    print(f"potato + gujarati = {result1}")
    
    result2 = service._get_fallback_translation('potato', 'Gujarati')
    print(f"potato + Gujarati = {result2}")
    
    # Test the full translate_text method
    print("\nTesting translate_text method:")
    result3 = service.translate_text('potato', 'Gujarati')
    print(f"translate_text('potato', 'Gujarati') = {result3}")

if __name__ == "__main__":
    test_fallback_lookup()