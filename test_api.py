#!/usr/bin/env python3
"""
Test the actual API endpoint to see if translations are working
"""

import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_vocabulary_api():
    """Test the vocabulary API endpoint"""
    try:
        # Test the vocabulary endpoint
        url = 'http://localhost:5000/api/vocabulary/2'  # Level 2 = animals
        
        print("Testing vocabulary API endpoint...")
        print(f"URL: {url}")
        
        response = requests.get(url)
        
        if response.status_code == 401:
            print("❌ API requires authentication. Need to be logged in.")
            return False
        elif response.status_code == 200:
            data = response.json()
            vocabulary = data.get('vocabulary', [])
            
            print(f"✅ API Response successful!")
            print(f"Found {len(vocabulary)} vocabulary items")
            
            # Show first 3 items
            for i, item in enumerate(vocabulary[:3]):
                print(f"{i+1}. {item.get('english')} -> {item.get('translation')}")
            
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is the Flask app running on localhost:5000?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_vocabulary_api()