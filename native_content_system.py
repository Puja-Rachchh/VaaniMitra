"""
Multi-Language Learning Content System
Provides native content for each Indian language (letters, vocabulary, etc.)
"""

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Native letter systems for each Indian language
LANGUAGE_LETTER_SYSTEMS = {
    'hindi': {
        'vowels': {
            'a': {'letter': 'अ', 'pronunciation': 'a', 'transliteration': 'a'},
            'aa': {'letter': 'आ', 'pronunciation': 'aa', 'transliteration': 'aa'},
            'i': {'letter': 'इ', 'pronunciation': 'i', 'transliteration': 'i'},
            'ii': {'letter': 'ई', 'pronunciation': 'ee', 'transliteration': 'ii'},
            'u': {'letter': 'उ', 'pronunciation': 'u', 'transliteration': 'u'},
            'uu': {'letter': 'ऊ', 'pronunciation': 'oo', 'transliteration': 'uu'},
            'e': {'letter': 'ए', 'pronunciation': 'ay', 'transliteration': 'e'},
            'ai': {'letter': 'ऐ', 'pronunciation': 'ai', 'transliteration': 'ai'},
            'o': {'letter': 'ओ', 'pronunciation': 'o', 'transliteration': 'o'},
            'au': {'letter': 'औ', 'pronunciation': 'au', 'transliteration': 'au'},
            'am': {'letter': 'अं', 'pronunciation': 'am', 'transliteration': 'am'},
            'aha': {'letter': 'अः', 'pronunciation': 'aha', 'transliteration': 'aha'}
        },
        'consonants': {
            'ka': {'letter': 'क', 'pronunciation': 'ka', 'transliteration': 'ka'},
            'kha': {'letter': 'ख', 'pronunciation': 'kha', 'transliteration': 'kha'},
            'ga': {'letter': 'ग', 'pronunciation': 'ga', 'transliteration': 'ga'},
            'gha': {'letter': 'घ', 'pronunciation': 'gha', 'transliteration': 'gha'},
            'cha': {'letter': 'च', 'pronunciation': 'cha', 'transliteration': 'cha'},
            'chha': {'letter': 'छ', 'pronunciation': 'chha', 'transliteration': 'chha'},
            'ja': {'letter': 'ज', 'pronunciation': 'ja', 'transliteration': 'ja'},
            'jha': {'letter': 'झ', 'pronunciation': 'jha', 'transliteration': 'jha'},
            'ta': {'letter': 'त', 'pronunciation': 'ta', 'transliteration': 'ta'},
            'tha': {'letter': 'थ', 'pronunciation': 'tha', 'transliteration': 'tha'},
            'da': {'letter': 'द', 'pronunciation': 'da', 'transliteration': 'da'},
            'dha': {'letter': 'ध', 'pronunciation': 'dha', 'transliteration': 'dha'},
            'na': {'letter': 'न', 'pronunciation': 'na', 'transliteration': 'na'},
            'pa': {'letter': 'प', 'pronunciation': 'pa', 'transliteration': 'pa'},
            'pha': {'letter': 'फ', 'pronunciation': 'pha', 'transliteration': 'pha'},
            'ba': {'letter': 'ब', 'pronunciation': 'ba', 'transliteration': 'ba'},
            'bha': {'letter': 'भ', 'pronunciation': 'bha', 'transliteration': 'bha'},
            'ma': {'letter': 'म', 'pronunciation': 'ma', 'transliteration': 'ma'},
            'ya': {'letter': 'य', 'pronunciation': 'ya', 'transliteration': 'ya'},
            'ra': {'letter': 'र', 'pronunciation': 'ra', 'transliteration': 'ra'},
            'la': {'letter': 'ल', 'pronunciation': 'la', 'transliteration': 'la'},
            'va': {'letter': 'व', 'pronunciation': 'va', 'transliteration': 'va'},
            'sha': {'letter': 'श', 'pronunciation': 'sha', 'transliteration': 'sha'},
            'sa': {'letter': 'स', 'pronunciation': 'sa', 'transliteration': 'sa'},
            'ha': {'letter': 'ह', 'pronunciation': 'ha', 'transliteration': 'ha'},
            'kshha': {'letter': 'क्ष', 'pronunciation': 'kshha', 'transliteration': 'kshha'},
            'tra': {'letter': 'त्र', 'pronunciation': 'tra', 'transliteration': 'tra'},
            'gna': {'letter': 'ज्ञ', 'pronunciation': 'gna', 'transliteration': 'gna'}
        }
    },
    
    'gujarati': {
        'vowels': {
            'a': {'letter': 'અ', 'pronunciation': 'a', 'transliteration': 'a'},
            'aa': {'letter': 'આ', 'pronunciation': 'aa', 'transliteration': 'aa'},
            'i': {'letter': 'ઇ', 'pronunciation': 'i', 'transliteration': 'i'},
            'ii': {'letter': 'ઈ', 'pronunciation': 'ee', 'transliteration': 'ii'},
            'u': {'letter': 'ઉ', 'pronunciation': 'u', 'transliteration': 'u'},
            'uu': {'letter': 'ઊ', 'pronunciation': 'oo', 'transliteration': 'uu'},
            'e': {'letter': 'એ', 'pronunciation': 'ay', 'transliteration': 'e'},
            'ai': {'letter': 'ઐ', 'pronunciation': 'ai', 'transliteration': 'ai'},
            'o': {'letter': 'ઓ', 'pronunciation': 'o', 'transliteration': 'o'},
            'au': {'letter': 'ઔ', 'pronunciation': 'au', 'transliteration': 'au'},
            'am': {'letter': 'અં', 'pronunciation': 'am', 'transliteration': 'am'},
            'aha': {'letter': 'અઃ', 'pronunciation': 'aha', 'transliteration': 'aha'}
        },
        'consonants': {
            'ka': {'letter': 'ક', 'pronunciation': 'ka', 'transliteration': 'ka'},
            'kha': {'letter': 'ખ', 'pronunciation': 'kha', 'transliteration': 'kha'},
            'ga': {'letter': 'ગ', 'pronunciation': 'ga', 'transliteration': 'ga'},
            'gha': {'letter': 'ઘ', 'pronunciation': 'gha', 'transliteration': 'gha'},
            'cha': {'letter': 'ચ', 'pronunciation': 'cha', 'transliteration': 'cha'},
            'chha': {'letter': 'છ', 'pronunciation': 'chha', 'transliteration': 'chha'},
            'ja': {'letter': 'જ', 'pronunciation': 'ja', 'transliteration': 'ja'},
            'jha': {'letter': 'ઝ', 'pronunciation': 'jha', 'transliteration': 'jha'},
            'tta': {'letter': 'ટ્ટ', 'pronunciation': 'tta', 'transliteration': 'tta'},
            'tha' :{'letter': 'ઠ', 'pronunciation': 'tha', 'transliteration': 'tha'},
            'da' :{'letter': 'ડ', 'pronunciation': 'da', 'transliteration': 'da'},
            'dha': {'letter': 'ઢ', 'pronunciation': 'dha', 'transliteration': 'dha'},
            'na': {'letter': 'ણ', 'pronunciation': 'na', 'transliteration': 'na'},
            'ta': {'letter': 'ત', 'pronunciation': 'ta', 'transliteration': 'ta'},
            'tha': {'letter': 'થ', 'pronunciation': 'tha', 'transliteration': 'tha'},
            'da': {'letter': 'દ', 'pronunciation': 'da', 'transliteration': 'da'},
            'dha': {'letter': 'ધ', 'pronunciation': 'dha', 'transliteration': 'dha'},
            'na': {'letter': 'ન', 'pronunciation': 'na', 'transliteration': 'na'},
            'pa': {'letter': 'પ', 'pronunciation': 'pa', 'transliteration': 'pa'},
            'pha': {'letter': 'ફ', 'pronunciation': 'pha', 'transliteration': 'pha'},
            'ba': {'letter': 'બ', 'pronunciation': 'ba', 'transliteration': 'ba'},
            'bha': {'letter': 'ભ', 'pronunciation': 'bha', 'transliteration': 'bha'},
            'ma': {'letter': 'મ', 'pronunciation': 'ma', 'transliteration': 'ma'},
            'ya': {'letter': 'ય', 'pronunciation': 'ya', 'transliteration': 'ya'},
            'ra': {'letter': 'ર', 'pronunciation': 'ra', 'transliteration': 'ra'},
            'la': {'letter': 'લ', 'pronunciation': 'la', 'transliteration': 'la'},
            'va': {'letter': 'વ', 'pronunciation': 'va', 'transliteration': 'va'},
            'sha': {'letter': 'શ', 'pronunciation': 'sha', 'transliteration': 'sha'},
            'sa': {'letter': 'સ', 'pronunciation': 'sa', 'transliteration': 'sa'},
            'ha': {'letter': 'હ', 'pronunciation': 'ha', 'transliteration': 'ha'},
            'kshha': {'letter': 'ક્ષ', 'pronunciation': 'kshha', 'transliteration': 'kshha'},
            'tra': {'letter': 'ત્ર', 'pronunciation': 'tra', 'transliteration': 'tra'},
            'gna': {'letter': 'ज्ञ', 'pronunciation': 'gna', 'transliteration': 'gna'}
        }
    },
    
    'tamil': {
        'vowels': {
            'a': {'letter': 'அ', 'pronunciation': 'a', 'transliteration': 'a'},
            'aa': {'letter': 'ஆ', 'pronunciation': 'aa', 'transliteration': 'aa'},
            'i': {'letter': 'இ', 'pronunciation': 'i', 'transliteration': 'i'},
            'ii': {'letter': 'ஈ', 'pronunciation': 'ee', 'transliteration': 'ii'},
            'u': {'letter': 'உ', 'pronunciation': 'u', 'transliteration': 'u'},
            'uu': {'letter': 'ஊ', 'pronunciation': 'oo', 'transliteration': 'uu'},
            'e': {'letter': 'எ', 'pronunciation': 'e', 'transliteration': 'e'},
            'ee': {'letter': 'ஏ', 'pronunciation': 'ee', 'transliteration': 'ee'},
            'ai': {'letter': 'ஐ', 'pronunciation': 'ai', 'transliteration': 'ai'},
            'o': {'letter': 'ஒ', 'pronunciation': 'o', 'transliteration': 'o'},
            'oo': {'letter': 'ஓ', 'pronunciation': 'oo', 'transliteration': 'oo'},
            'au': {'letter': 'ஔ', 'pronunciation': 'au', 'transliteration': 'au'},
            'am': {'letter': 'அம்', 'pronunciation': 'am', 'transliteration': 'am'},
            'aha': {'letter': 'அஃ', 'pronunciation': 'aha', 'transliteration': 'aha'}
        },
        'consonants': {
            'ka': {'letter': 'க', 'pronunciation': 'ka', 'transliteration': 'ka'},
            'nga': {'letter': 'ங', 'pronunciation': 'nga', 'transliteration': 'nga'},
            'cha': {'letter': 'ச', 'pronunciation': 'cha', 'transliteration': 'cha'},
            'ja': {'letter': 'ஜ', 'pronunciation': 'ja', 'transliteration': 'ja'},
            'nya': {'letter': 'ஞ', 'pronunciation': 'nya', 'transliteration': 'nya'},
            'ta': {'letter': 'ட', 'pronunciation': 'ta', 'transliteration': 'ta'},
            'na': {'letter': 'ண', 'pronunciation': 'na', 'transliteration': 'na'},
            'tha': {'letter': 'த', 'pronunciation': 'tha', 'transliteration': 'tha'},
            'nna': {'letter': 'ந', 'pronunciation': 'nna', 'transliteration': 'nna'},
            'pa': {'letter': 'ப', 'pronunciation': 'pa', 'transliteration': 'pa'},
            'ma': {'letter': 'ம', 'pronunciation': 'ma', 'transliteration': 'ma'},
            'ya': {'letter': 'ய', 'pronunciation': 'ya', 'transliteration': 'ya'},
            'ra': {'letter': 'ர', 'pronunciation': 'ra', 'transliteration': 'ra'},
            'la': {'letter': 'ல', 'pronunciation': 'la', 'transliteration': 'la'},
            'va': {'letter': 'வ', 'pronunciation': 'va', 'transliteration': 'va'},
            'sha': {'letter': 'ஷ', 'pronunciation': 'sha', 'transliteration': 'sha'},
            'sa': {'letter': 'ச', 'pronunciation': 'sa', 'transliteration': 'sa'},
            'ha': {'letter': 'ஹ', 'pronunciation': 'ha', 'transliteration': 'ha'},
            'zha': {'letter': 'ழ', 'pronunciation': 'zha', 'transliteration': 'zha'},
            'llla': {'letter': 'ள', 'pronunciation': 'llla', 'transliteration': 'llla'},
            'rra': {'letter': 'ற', 'pronunciation': 'rra', 'transliteration': 'rra'},
            'nnn': {'letter': 'ன', 'pronunciation': 'nnn', 'transliteration': 'nnn'},
        
        }
    },
    
    'bengali': {
        'vowels': {
            'a': {'letter': 'অ', 'pronunciation': 'a', 'transliteration': 'a'},
            'aa': {'letter': 'আ', 'pronunciation': 'aa', 'transliteration': 'aa'},
            'i': {'letter': 'ই', 'pronunciation': 'i', 'transliteration': 'i'},
            'ii': {'letter': 'ঈ', 'pronunciation': 'ee', 'transliteration': 'ii'},
            'u': {'letter': 'উ', 'pronunciation': 'u', 'transliteration': 'u'},
            'uu': {'letter': 'ঊ', 'pronunciation': 'oo', 'transliteration': 'uu'},
            'e': {'letter': 'এ', 'pronunciation': 'e', 'transliteration': 'e'},
            'ai': {'letter': 'ঐ', 'pronunciation': 'ai', 'transliteration': 'ai'},
            'o': {'letter': 'ও', 'pronunciation': 'o', 'transliteration': 'o'},
            'au': {'letter': 'ঔ', 'pronunciation': 'au', 'transliteration': 'au'}
        },
        'consonants': {
            'ka': {'letter': 'ক', 'pronunciation': 'ka', 'transliteration': 'ka'},
            'kha': {'letter': 'খ', 'pronunciation': 'kha', 'transliteration': 'kha'},
            'ga': {'letter': 'গ', 'pronunciation': 'ga', 'transliteration': 'ga'},
            'gha': {'letter': 'ঘ', 'pronunciation': 'gha', 'transliteration': 'gha'},
            'nga': {'letter': 'ঙ', 'pronunciation': 'nga', 'transliteration': 'nga'},
            'cha': {'letter': 'চ', 'pronunciation': 'cha', 'transliteration': 'cha'},
            'chha': {'letter': 'ছ', 'pronunciation': 'chha', 'transliteration': 'chha'},
            'ja': {'letter': 'জ', 'pronunciation': 'ja', 'transliteration': 'ja'},
            'jha': {'letter': 'ঝ', 'pronunciation': 'jha', 'transliteration': 'jha'},
            'nya': {'letter': 'ঞ', 'pronunciation': 'nya', 'transliteration': 'nya'},
            'ta': {'letter': 'ত', 'pronunciation': 'ta', 'transliteration': 'ta'},
            'tha': {'letter': 'থ', 'pronunciation': 'tha', 'transliteration': 'tha'},
            'da': {'letter': 'দ', 'pronunciation': 'da', 'transliteration': 'da'},
            'dha': {'letter': 'ধ', 'pronunciation': 'dha', 'transliteration': 'dha'},
            'na': {'letter': 'ন', 'pronunciation': 'na', 'transliteration': 'na'},
            'pa': {'letter': 'প', 'pronunciation': 'pa', 'transliteration': 'pa'},
            'pha': {'letter': 'ফ', 'pronunciation': 'pha', 'transliteration': 'pha'},
            'ba': {'letter': 'ব', 'pronunciation': 'ba', 'transliteration': 'ba'},
            'bha': {'letter': 'ভ', 'pronunciation': 'bha', 'transliteration': 'bha'},
            'ma': {'letter': 'ম', 'pronunciation': 'ma', 'transliteration': 'ma'},
            'ya': {'letter': 'য', 'pronunciation': 'ya', 'transliteration': 'ya'},
            'ra': {'letter': 'র', 'pronunciation': 'ra', 'transliteration': 'ra'},
            'la': {'letter': 'ল', 'pronunciation': 'la', 'transliteration': 'la'},
            'sha': {'letter': 'শ', 'pronunciation': 'sha', 'transliteration': 'sha'},
            'ssa': {'letter': 'ষ', 'pronunciation': 'ssa', 'transliteration': 'ssa'},
            'sa': {'letter': 'স', 'pronunciation': 'sa', 'transliteration': 'sa'},
            'ha': {'letter': 'হ', 'pronunciation': 'ha', 'transliteration': 'ha'}
        }
    },
    
    'telugu': {
        'vowels': {
            'a': {'letter': 'అ', 'pronunciation': 'a', 'transliteration': 'a'},
            'aa': {'letter': 'ఆ', 'pronunciation': 'aa', 'transliteration': 'aa'},
            'i': {'letter': 'ఇ', 'pronunciation': 'i', 'transliteration': 'i'},
            'ii': {'letter': 'ఈ', 'pronunciation': 'ee', 'transliteration': 'ii'},
            'u': {'letter': 'ఉ', 'pronunciation': 'u', 'transliteration': 'u'},
            'uu': {'letter': 'ఊ', 'pronunciation': 'oo', 'transliteration': 'uu'},
            'e': {'letter': 'ఎ', 'pronunciation': 'e', 'transliteration': 'e'},
            'ee': {'letter': 'ఏ', 'pronunciation': 'ee', 'transliteration': 'ee'},
            'ai': {'letter': 'ఐ', 'pronunciation': 'ai', 'transliteration': 'ai'},
            'o': {'letter': 'ఒ', 'pronunciation': 'o', 'transliteration': 'o'},
            'oo': {'letter': 'ఓ', 'pronunciation': 'oo', 'transliteration': 'oo'},
            'au': {'letter': 'ఔ', 'pronunciation': 'au', 'transliteration': 'au'}
        },
        'consonants': {
            'ka': {'letter': 'క', 'pronunciation': 'ka', 'transliteration': 'ka'},
            'kha': {'letter': 'ఖ', 'pronunciation': 'kha', 'transliteration': 'kha'},
            'ga': {'letter': 'గ', 'pronunciation': 'ga', 'transliteration': 'ga'},
            'gha': {'letter': 'ఘ', 'pronunciation': 'gha', 'transliteration': 'gha'},
            'nga': {'letter': 'ఙ', 'pronunciation': 'nga', 'transliteration': 'nga'},
            'cha': {'letter': 'చ', 'pronunciation': 'cha', 'transliteration': 'cha'},
            'chha': {'letter': 'ఛ', 'pronunciation': 'chha', 'transliteration': 'chha'},
            'ja': {'letter': 'జ', 'pronunciation': 'ja', 'transliteration': 'ja'},
            'jha': {'letter': 'ఝ', 'pronunciation': 'jha', 'transliteration': 'jha'},
            'nya': {'letter': 'ఞ', 'pronunciation': 'nya', 'transliteration': 'nya'},
            'ta': {'letter': 'త', 'pronunciation': 'ta', 'transliteration': 'ta'},
            'tha': {'letter': 'థ', 'pronunciation': 'tha', 'transliteration': 'tha'},
            'da': {'letter': 'ద', 'pronunciation': 'da', 'transliteration': 'da'},
            'dha': {'letter': 'ధ', 'pronunciation': 'dha', 'transliteration': 'dha'},
            'na': {'letter': 'న', 'pronunciation': 'na', 'transliteration': 'na'},
            'pa': {'letter': 'ప', 'pronunciation': 'pa', 'transliteration': 'pa'},
            'pha': {'letter': 'ఫ', 'pronunciation': 'pha', 'transliteration': 'pha'},
            'ba': {'letter': 'బ', 'pronunciation': 'ba', 'transliteration': 'ba'},
            'bha': {'letter': 'భ', 'pronunciation': 'bha', 'transliteration': 'bha'},
            'ma': {'letter': 'మ', 'pronunciation': 'ma', 'transliteration': 'ma'},
            'ya': {'letter': 'య', 'pronunciation': 'ya', 'transliteration': 'ya'},
            'ra': {'letter': 'ర', 'pronunciation': 'ra', 'transliteration': 'ra'},
            'la': {'letter': 'ల', 'pronunciation': 'la', 'transliteration': 'la'},
            'va': {'letter': 'వ', 'pronunciation': 'va', 'transliteration': 'va'},
            'sha': {'letter': 'శ', 'pronunciation': 'sha', 'transliteration': 'sha'},
            'ssa': {'letter': 'ష', 'pronunciation': 'ssa', 'transliteration': 'ssa'},
            'sa': {'letter': 'స', 'pronunciation': 'sa', 'transliteration': 'sa'},
            'ha': {'letter': 'హ', 'pronunciation': 'ha', 'transliteration': 'ha'}
        }
    }
}

# English base vocabulary for automatic translation
# All vocabulary will be automatically translated to target languages using IndicTrans2
ENGLISH_BASE_VOCABULARY = {
    'fruits': [
        'apple', 'banana', 'mango', 'orange', 'grapes', 'watermelon', 
        'pomegranate', 'guava', 'pear', 'lemon', 'pineapple', 'strawberry',
        'cherry', 'peach', 'plum', 'apricot', 'coconut', 'papaya',
        'kiwi', 'avocado', 'dates', 'figs', 'jackfruit', 'litchi'
    ],
    'animals': [
        'dog', 'cat', 'cow', 'horse', 'lion', 'tiger', 'elephant', 
        'monkey', 'bear', 'fox', 'rabbit', 'deer', 'goat', 'sheep',
        'pig', 'duck', 'chicken', 'peacock', 'parrot', 'eagle',
        'snake', 'frog', 'fish', 'butterfly', 'ant', 'bee'
    ],
    'colors': [
        'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink',
        'white', 'black', 'brown', 'gray', 'violet', 'indigo', 'cyan',
        'magenta', 'maroon', 'navy', 'olive', 'silver', 'gold'
    ],
    'numbers': [
        'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
        'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
        'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty'
    ],
    'body_parts': [
        'head', 'eye', 'nose', 'mouth', 'ear', 'hand', 'foot', 'arm',
        'leg', 'finger', 'toe', 'hair', 'tooth', 'tongue', 'neck',
        'shoulder', 'chest', 'back', 'stomach', 'knee'
    ],
    'family': [
        'mother', 'father', 'brother', 'sister', 'grandmother', 'grandfather',
        'uncle', 'aunt', 'cousin', 'son', 'daughter', 'husband', 'wife',
        'nephew', 'niece', 'father-in-law', 'mother-in-law', 'sister-in-law', 'brother-in-law'
    ],
    'vegetables': [
        'potato', 'tomato', 'onion', 'carrot', 'cabbage', 'spinach',
        'broccoli', 'cauliflower', 'peas', 'beans', 'corn', 'cucumber',
        'bell pepper', 'eggplant', 'okra', 'garlic', 'ginger', 'chili'
    ],
    'professionals': [
        'doctor', 'teacher', 'engineer', 'nurse', 'police', 'farmer',
        'driver', 'chef', 'lawyer', 'banker'
    ]
}

def get_language_letters(target_language):
    """Get native letters for the target language user wants to learn"""
    # Convert to lowercase to handle case variations
    target_language = target_language.lower() if target_language else ''
    return LANGUAGE_LETTER_SYSTEMS.get(target_language, LANGUAGE_LETTER_SYSTEMS['hindi'])

def get_english_vocabulary(category):
    """Get English vocabulary for a specific category"""
    return ENGLISH_BASE_VOCABULARY.get(category, [])

def get_all_vocabulary_categories():
    """Get list of all available vocabulary categories"""
    return list(ENGLISH_BASE_VOCABULARY.keys())

def get_translated_vocabulary(target_language, category):
    """
    Get vocabulary translated to target language using IndicTrans2
    This function will be called by routes that import the translation service
    """
    english_words = get_english_vocabulary(category)
    if not english_words:
        return []
    
    # Return English words - translation will be handled by the route
    # that has access to the translation service
    return english_words

def get_all_supported_target_languages():
    """Get list of languages that can be learned (have native content)"""
    return list(LANGUAGE_LETTER_SYSTEMS.keys())

def format_learning_content(target_language, known_language, content_type, category=None):
    """
    Format learning content for target language with explanations in known language
    
    Args:
        target_language: Language user wants to learn (e.g., 'gujarati')
        known_language: Language user already knows (e.g., 'english') 
        content_type: 'letters' or 'vocabulary'
        category: For vocabulary - 'fruits', 'animals', etc.
    """
    try:
        if content_type == 'letters':
            letters = get_language_letters(target_language)
            return letters
        elif content_type == 'vocabulary':
            # Return English words - translation handled by calling code
            english_words = get_english_vocabulary(category)
            return english_words
        else:
            return {}
    except Exception as e:
        logger.error(f"Error formatting learning content: {e}")
        return {}

if __name__ == "__main__":
    # Test the system
    print("Testing Multi-Language Learning Content...")
    
    # Test Gujarati letters
    gujarati_letters = get_language_letters('gujarati')
    print(f"\nGujarati Vowels: {list(gujarati_letters['vowels'].keys())[:5]}...")
    print(f"First Gujarati Consonant: {gujarati_letters['consonants']['ka']}")
    
    # Test English vocabulary
    fruits = get_english_vocabulary('fruits')
    print(f"\nEnglish Fruits: {fruits[:5]}...")
    
    # Test vocabulary categories
    categories = get_all_vocabulary_categories()
    print(f"\nAvailable Categories: {categories}")
    
    print(f"\nSupported target languages: {get_all_supported_target_languages()}")