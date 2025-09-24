#!/usr/bin/env python3
"""
Quick test to debug fallback translations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from indictrans2_service import get_translation_service

def test_fallback():
    service = get_translation_service()
    
    # Test fallback directly
    result = service._get_fallback_translation('apple', 'gujarati')
    print(f"Fallback result for 'apple' in Gujarati: {result}")
    
    # Test if fallback translations are loaded
    print(f"Fallback translations loaded: {bool(service.fallback_translations)}")
    print(f"Available categories: {list(service.fallback_translations.keys())}")
    
    if 'fruits' in service.fallback_translations:
        print(f"Available fruits: {list(service.fallback_translations['fruits'].keys())}")
        if 'apple' in service.fallback_translations['fruits']:
            print(f"Apple translations: {service.fallback_translations['fruits']['apple']}")

if __name__ == "__main__":
    test_fallback()