"""
Test script for IndicTrans2 Translation Service
"""

import sys
import os

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_translation_service():
    """Test the translation service functionality"""
    print("Testing IndicTrans2 Translation Service...")
    
    try:
        from translation_service import IndicTrans2Service
        
        # Initialize translator
        print("Initializing translator...")
        translator = IndicTrans2Service()
        
        # Test single translation
        print("\n=== Testing Single Translation ===")
        test_text = "Hello, how are you?"
        target_language = "hindi"
        
        print(f"Original text: {test_text}")
        print(f"Target language: {target_language}")
        
        translation = translator.translate_text(test_text, target_language)
        print(f"Translation: {translation}")
        
        # Test batch translation
        print("\n=== Testing Batch Translation ===")
        test_texts = ["Dog", "Cat", "Elephant", "Apple", "Red", "Blue"]
        target_language = "tamil"
        
        print(f"Original texts: {test_texts}")
        print(f"Target language: {target_language}")
        
        translations = translator.translate_batch(test_texts, target_language)
        
        for original, translated in zip(test_texts, translations):
            print(f"{original} -> {translated}")
        
        # Test vocabulary translation
        print("\n=== Testing Vocabulary Translation ===")
        sample_vocab = {
            'animals': {
                'dog': {'english': 'Dog'},
                'cat': {'english': 'Cat'},
                'elephant': {'english': 'Elephant'}
            },
            'colors': {
                'red': {'english': 'Red'},
                'blue': {'english': 'Blue'},
                'green': {'english': 'Green'}
            }
        }
        
        print("Translating vocabulary to multiple languages...")
        multilingual_vocab = translator.translate_vocabulary(
            sample_vocab, 
            target_languages=['hindi', 'tamil', 'bengali']
        )
        
        print("\nMultilingual Vocabulary:")
        for category, items in multilingual_vocab.items():
            print(f"\n{category.upper()}:")
            for key, data in items.items():
                print(f"  {key}:")
                print(f"    English: {data['english']}")
                for lang, translation in data['translations'].items():
                    print(f"    {lang.title()}: {translation}")
        
        print("\n✅ Translation service test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Translation service test failed: {e}")
        return False

def test_without_model():
    """Test without loading the full model (for CI/CD environments)"""
    print("Testing translation service structure...")
    
    try:
        from translation_service import IndicTrans2Service
        
        # Just test the class structure without loading model
        translator = IndicTrans2Service.__new__(IndicTrans2Service)
        translator.supported_languages = {
            'hindi': 'hin_Deva',
            'tamil': 'tam_Taml',
            'bengali': 'ben_Beng'
        }
        
        # Test language list
        languages = translator.get_available_languages()
        print(f"Supported languages: {languages}")
        
        print("✅ Translation service structure test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Translation service structure test failed: {e}")
        return False

if __name__ == "__main__":
    print("VaaniMitra Translation Service Test")
    print("=" * 50)
    
    # Check if we have GPU support
    try:
        import torch
        if torch.cuda.is_available():
            print(f"🚀 CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("💻 Using CPU (CUDA not available)")
    except ImportError:
        print("⚠️  PyTorch not installed")
    
    print("\nChoose test mode:")
    print("1. Full test with model loading (requires good internet and time)")
    print("2. Structure test only (quick)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        success = test_translation_service()
    else:
        success = test_without_model()
    
    if success:
        print("\n🎉 All tests passed! Translation service is ready to use.")
    else:
        print("\n❌ Some tests failed. Please check the setup.")