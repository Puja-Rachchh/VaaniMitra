#!/usr/bin/env python3
"""
Test script to verify the pronunciation evaluation API endpoint
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_pronunciation_api():
    """Test the pronunciation evaluation API endpoint"""
    print("🧪 Testing Pronunciation Evaluation API...")
    
    with app.test_client() as client:
        with app.app_context():
            # Create a test session (simulate logged in user)
            with client.session_transaction() as sess:
                sess['user'] = 'test_user'
            
            # Test data for pronunciation evaluation
            test_data = {
                'spoken_text': 'kutta',
                'expected_variants': ['kutta', 'dog', 'kutaa']
            }
            
            print(f"Sending request with data: {test_data}")
            
            # Make POST request to the API
            response = client.post('/api/evaluate-pronunciation',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.get_json()
                print(f"✅ Success! Response: {result}")
                print(f"   Score: {result.get('score', 'N/A')}%")
                print(f"   Feedback: {result.get('feedback', 'N/A')}")
                print(f"   Status: {result.get('status', 'N/A')}")
            else:
                result = response.get_json()
                print(f"❌ Error: {result}")
            
            return response.status_code == 200

def test_pronunciation_data_api():
    """Test the pronunciation data API endpoint"""
    print("\n🔍 Testing Pronunciation Data API...")
    
    with app.test_client() as client:
        with app.app_context():
            # Create a test session (simulate logged in user)
            with client.session_transaction() as sess:
                sess['user'] = 'test_user'
            
            # Test data for getting pronunciation data
            test_data = {
                'word': 'dog',
                'language': 'Hindi'
            }
            
            print(f"Sending request with data: {test_data}")
            
            # Make POST request to the API
            response = client.post('/api/get-pronunciation-data',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.get_json()
                print(f"✅ Success! Response: {result}")
                print(f"   English: {result.get('english', 'N/A')}")
                print(f"   Translation: {result.get('translation', 'N/A')}")
                print(f"   Pronunciation: {result.get('pronunciation', 'N/A')}")
                print(f"   Variants: {result.get('variants', 'N/A')}")
            else:
                result = response.get_json()
                print(f"❌ Error: {result}")
            
            return response.status_code == 200

if __name__ == "__main__":
    print("🚀 Testing Pronunciation APIs")
    print("=" * 50)
    
    try:
        # Import a mock user for testing
        from mongodb_models import User
        
        # Create a mock user object for testing
        mock_user = User()
        mock_user.username = 'test_user'
        mock_user.target_language = 'Hindi'
        
        # Test both APIs
        test1_passed = test_pronunciation_data_api()
        test2_passed = test_pronunciation_api()
        
        if test1_passed and test2_passed:
            print("\n🎉 All pronunciation API tests passed!")
        else:
            print("\n⚠️ Some tests failed - check the output above")
    
    except Exception as e:
        print(f"\n❌ Test setup failed: {e}")
        print("Note: This is expected if user doesn't exist in database")
        print("The APIs should still work when accessed through the web interface")