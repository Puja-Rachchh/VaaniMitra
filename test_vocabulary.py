#!/usr/bin/env python3
"""
Test script to check MongoDB vocabulary retrieval
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from mongodb_models import MultilingualVocabulary

def test_vocabulary_retrieval():
    """Test vocabulary retrieval from MongoDB"""
    with app.app_context():
        try:
            print("Testing vocabulary retrieval from MongoDB...")
            
            # Test animals category with Hindi
            vocab = MultilingualVocabulary.get_vocabulary_by_category('animals', 'hindi')
            print(f"\nFound {len(vocab)} animals in Hindi:")
            
            for i, item in enumerate(vocab[:5]):
                print(f"{i+1}. {item['english']} -> {item['translation']}")
            
            # Test what happens with a user's target_language
            print("\n" + "="*50)
            print("Testing with different language formats:")
            
            # Test with 'Hindi' (capitalized)
            vocab2 = MultilingualVocabulary.get_vocabulary_by_category('animals', 'Hindi')
            print(f"With 'Hindi': Found {len(vocab2)} animals")
            if vocab2:
                print(f"Sample: {vocab2[0]['english']} -> {vocab2[0]['translation']}")
            
            # Test with 'hindi' (lowercase)  
            vocab3 = MultilingualVocabulary.get_vocabulary_by_category('animals', 'hindi')
            print(f"With 'hindi': Found {len(vocab3)} animals")
            if vocab3:
                print(f"Sample: {vocab3[0]['english']} -> {vocab3[0]['translation']}")
            
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            return False

if __name__ == "__main__":
    test_vocabulary_retrieval()