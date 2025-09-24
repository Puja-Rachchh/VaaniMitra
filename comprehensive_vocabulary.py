"""
Enhanced vocabulary data for all levels with comprehensive content
Supports translation from English to all Indian languages
"""

from translation_service import get_translator
from mongodb_models import MultilingualVocabulary, get_database
import logging

logger = logging.getLogger(__name__)

# Comprehensive vocabulary data for all levels
COMPREHENSIVE_VOCABULARY = {
    # Beginner Level - Hindi Letters/Vowels/Consonants
    'hindi_vowels': {
        'a': {'english': 'अ', 'pronunciation': 'a', 'description': 'Short vowel sound like in "but"'},
        'aa': {'english': 'आ', 'pronunciation': 'aa', 'description': 'Long vowel sound like in "father"'},
        'i': {'english': 'इ', 'pronunciation': 'i', 'description': 'Short vowel sound like in "bit"'},
        'ii': {'english': 'ई', 'pronunciation': 'ee', 'description': 'Long vowel sound like in "beet"'},
        'u': {'english': 'उ', 'pronunciation': 'u', 'description': 'Short vowel sound like in "put"'},
        'uu': {'english': 'ऊ', 'pronunciation': 'oo', 'description': 'Long vowel sound like in "boot"'},
        'e': {'english': 'ए', 'pronunciation': 'ay', 'description': 'Vowel sound like in "bay"'},
        'ai': {'english': 'ऐ', 'pronunciation': 'ai', 'description': 'Vowel sound like in "bye"'},
        'o': {'english': 'ओ', 'pronunciation': 'o', 'description': 'Vowel sound like in "go"'},
        'au': {'english': 'औ', 'pronunciation': 'au', 'description': 'Vowel sound like in "cow"'}
    },
    
    'hindi_consonants': {
        'ka': {'english': 'क', 'pronunciation': 'ka', 'description': 'Consonant k sound'},
        'kha': {'english': 'ख', 'pronunciation': 'kha', 'description': 'Aspirated k sound'},
        'ga': {'english': 'ग', 'pronunciation': 'ga', 'description': 'Consonant g sound'},
        'gha': {'english': 'घ', 'pronunciation': 'gha', 'description': 'Aspirated g sound'},
        'cha': {'english': 'च', 'pronunciation': 'cha', 'description': 'Consonant ch sound'},
        'chha': {'english': 'छ', 'pronunciation': 'chha', 'description': 'Aspirated ch sound'},
        'ja': {'english': 'ज', 'pronunciation': 'ja', 'description': 'Consonant j sound'},
        'jha': {'english': 'झ', 'pronunciation': 'jha', 'description': 'Aspirated j sound'},
        'ta': {'english': 'त', 'pronunciation': 'ta', 'description': 'Consonant t sound'},
        'tha': {'english': 'थ', 'pronunciation': 'tha', 'description': 'Aspirated t sound'},
        'da': {'english': 'द', 'pronunciation': 'da', 'description': 'Consonant d sound'},
        'dha': {'english': 'ध', 'pronunciation': 'dha', 'description': 'Aspirated d sound'},
        'na': {'english': 'न', 'pronunciation': 'na', 'description': 'Consonant n sound'},
        'pa': {'english': 'प', 'pronunciation': 'pa', 'description': 'Consonant p sound'},
        'pha': {'english': 'फ', 'pronunciation': 'pha', 'description': 'Aspirated p sound'},
        'ba': {'english': 'ब', 'pronunciation': 'ba', 'description': 'Consonant b sound'},
        'bha': {'english': 'भ', 'pronunciation': 'bha', 'description': 'Aspirated b sound'},
        'ma': {'english': 'म', 'pronunciation': 'ma', 'description': 'Consonant m sound'},
        'ya': {'english': 'य', 'pronunciation': 'ya', 'description': 'Consonant y sound'},
        'ra': {'english': 'र', 'pronunciation': 'ra', 'description': 'Consonant r sound'},
        'la': {'english': 'ल', 'pronunciation': 'la', 'description': 'Consonant l sound'},
        'va': {'english': 'व', 'pronunciation': 'va', 'description': 'Consonant v sound'},
        'sha': {'english': 'श', 'pronunciation': 'sha', 'description': 'Consonant sh sound'},
        'sa': {'english': 'स', 'pronunciation': 'sa', 'description': 'Consonant s sound'},
        'ha': {'english': 'ह', 'pronunciation': 'ha', 'description': 'Consonant h sound'}
    },

    # Intermediate Level 1 - Fruits and Vegetables
    'fruits': {
        'apple': {'english': 'Apple', 'pronunciation': 'seb'},
        'banana': {'english': 'Banana', 'pronunciation': 'kela'},
        'mango': {'english': 'Mango', 'pronunciation': 'aam'},
        'orange': {'english': 'Orange', 'pronunciation': 'santra'},
        'grapes': {'english': 'Grapes', 'pronunciation': 'angoor'},
        'strawberry': {'english': 'Strawberry', 'pronunciation': 'strawberry'},
        'pineapple': {'english': 'Pineapple', 'pronunciation': 'ananas'},
        'watermelon': {'english': 'Watermelon', 'pronunciation': 'tarbooz'},
        'papaya': {'english': 'Papaya', 'pronunciation': 'papita'},
        'coconut': {'english': 'Coconut', 'pronunciation': 'nariyal'},
        'lemon': {'english': 'Lemon', 'pronunciation': 'nimbu'},
        'pomegranate': {'english': 'Pomegranate', 'pronunciation': 'anar'},
        'guava': {'english': 'Guava', 'pronunciation': 'amrood'},
        'cherry': {'english': 'Cherry', 'pronunciation': 'cherry'},
        'kiwi': {'english': 'Kiwi', 'pronunciation': 'kiwi'},
        'pear': {'english': 'Pear', 'pronunciation': 'nashpati'},
        'peach': {'english': 'Peach', 'pronunciation': 'aadu'},
        'plum': {'english': 'Plum', 'pronunciation': 'aloo bukhara'},
        'dates': {'english': 'Dates', 'pronunciation': 'khajoor'},
        'fig': {'english': 'Fig', 'pronunciation': 'anjeer'},
        'lychee': {'english': 'Lychee', 'pronunciation': 'litchi'},
        'jackfruit': {'english': 'Jackfruit', 'pronunciation': 'kathal'},
        'custard_apple': {'english': 'Custard Apple', 'pronunciation': 'shareefa'},
        'dragon_fruit': {'english': 'Dragon Fruit', 'pronunciation': 'dragon fruit'},
        'avocado': {'english': 'Avocado', 'pronunciation': 'avocado'},
        'apricot': {'english': 'Apricot', 'pronunciation': 'khurmani'},
        'blackberry': {'english': 'Blackberry', 'pronunciation': 'blackberry'}
    },

    'vegetables': {
        'potato': {'english': 'Potato', 'pronunciation': 'aloo'},
        'onion': {'english': 'Onion', 'pronunciation': 'pyaz'},
        'tomato': {'english': 'Tomato', 'pronunciation': 'tamatar'},
        'carrot': {'english': 'Carrot', 'pronunciation': 'gajar'},
        'cabbage': {'english': 'Cabbage', 'pronunciation': 'patta gobhi'},
        'cauliflower': {'english': 'Cauliflower', 'pronunciation': 'phool gobhi'},
        'brinjal': {'english': 'Brinjal', 'pronunciation': 'baingan'},
        'okra': {'english': 'Okra', 'pronunciation': 'bhindi'},
        'spinach': {'english': 'Spinach', 'pronunciation': 'palak'},
        'peas': {'english': 'Peas', 'pronunciation': 'matar'},
        'cucumber': {'english': 'Cucumber', 'pronunciation': 'kheera'},
        'radish': {'english': 'Radish', 'pronunciation': 'mooli'},
        'beetroot': {'english': 'Beetroot', 'pronunciation': 'chukandar'},
        'ginger': {'english': 'Ginger', 'pronunciation': 'adrak'},
        'garlic': {'english': 'Garlic', 'pronunciation': 'lehsun'},
        'green_chili': {'english': 'Green Chili', 'pronunciation': 'hari mirch'},
        'capsicum': {'english': 'Capsicum', 'pronunciation': 'shimla mirch'},
        'corn': {'english': 'Corn', 'pronunciation': 'makka'},
        'pumpkin': {'english': 'Pumpkin', 'pronunciation': 'kaddu'},
        'bottle_gourd': {'english': 'Bottle Gourd', 'pronunciation': 'lauki'},
        'bitter_gourd': {'english': 'Bitter Gourd', 'pronunciation': 'karela'},
        'ridge_gourd': {'english': 'Ridge Gourd', 'pronunciation': 'turai'},
        'drumstick': {'english': 'Drumstick', 'pronunciation': 'sahjan'},
        'fenugreek': {'english': 'Fenugreek', 'pronunciation': 'methi'},
        'coriander': {'english': 'Coriander', 'pronunciation': 'dhaniya'},
        'mint': {'english': 'Mint', 'pronunciation': 'pudina'},
        'mushroom': {'english': 'Mushroom', 'pronunciation': 'khumbi'}
    },

    # Intermediate Level 2 - Animals and Birds
    'animals': {
        'dog': {'english': 'Dog', 'pronunciation': 'kutta'},
        'cat': {'english': 'Cat', 'pronunciation': 'billi'},
        'cow': {'english': 'Cow', 'pronunciation': 'gaay'},
        'horse': {'english': 'Horse', 'pronunciation': 'ghoda'},
        'goat': {'english': 'Goat', 'pronunciation': 'bakri'},
        'sheep': {'english': 'Sheep', 'pronunciation': 'bhed'},
        'pig': {'english': 'Pig', 'pronunciation': 'suar'},
        'lion': {'english': 'Lion', 'pronunciation': 'sher'},
        'tiger': {'english': 'Tiger', 'pronunciation': 'baagh'},
        'elephant': {'english': 'Elephant', 'pronunciation': 'haathi'},
        'bear': {'english': 'Bear', 'pronunciation': 'bhaalu'},
        'monkey': {'english': 'Monkey', 'pronunciation': 'bandar'},
        'fox': {'english': 'Fox', 'pronunciation': 'lomdi'},
        'rabbit': {'english': 'Rabbit', 'pronunciation': 'khargosh'},
        'deer': {'english': 'Deer', 'pronunciation': 'hiran'},
        'camel': {'english': 'Camel', 'pronunciation': 'oont'},
        'buffalo': {'english': 'Buffalo', 'pronunciation': 'bhains'},
        'donkey': {'english': 'Donkey', 'pronunciation': 'gadha'},
        'mouse': {'english': 'Mouse', 'pronunciation': 'chuha'},
        'rat': {'english': 'Rat', 'pronunciation': 'chuha'},
        'snake': {'english': 'Snake', 'pronunciation': 'saanp'},
        'frog': {'english': 'Frog', 'pronunciation': 'mendak'},
        'fish': {'english': 'Fish', 'pronunciation': 'machli'},
        'turtle': {'english': 'Turtle', 'pronunciation': 'kachua'},
        'crocodile': {'english': 'Crocodile', 'pronunciation': 'magarmach'},
        'rhinoceros': {'english': 'Rhinoceros', 'pronunciation': 'gainda'},
        'hippopotamus': {'english': 'Hippopotamus', 'pronunciation': 'dariyai ghoda'},
        'giraffe': {'english': 'Giraffe', 'pronunciation': 'jiraaf'},
        'zebra': {'english': 'Zebra', 'pronunciation': 'zebra'},
        'leopard': {'english': 'Leopard', 'pronunciation': 'cheetah'},
        'wolf': {'english': 'Wolf', 'pronunciation': 'bhediya'},
        'jackal': {'english': 'Jackal', 'pronunciation': 'geedh'},
        'hyena': {'english': 'Hyena', 'pronunciation': 'lakadbaggha'},
        'squirrel': {'english': 'Squirrel', 'pronunciation': 'gilhari'},
        'porcupine': {'english': 'Porcupine', 'pronunciation': 'saahi'}
    },

    'birds': {
        'peacock': {'english': 'Peacock', 'pronunciation': 'mor'},
        'parrot': {'english': 'Parrot', 'pronunciation': 'tota'},
        'crow': {'english': 'Crow', 'pronunciation': 'kauwa'},
        'sparrow': {'english': 'Sparrow', 'pronunciation': 'gauraiya'},
        'eagle': {'english': 'Eagle', 'pronunciation': 'baaz'},
        'owl': {'english': 'Owl', 'pronunciation': 'ullu'},
        'pigeon': {'english': 'Pigeon', 'pronunciation': 'kabutar'},
        'duck': {'english': 'Duck', 'pronunciation': 'battakh'},
        'swan': {'english': 'Swan', 'pronunciation': 'hans'},
        'hen': {'english': 'Hen', 'pronunciation': 'murgi'},
        'rooster': {'english': 'Rooster', 'pronunciation': 'murga'},
        'vulture': {'english': 'Vulture', 'pronunciation': 'gidh'},
        'crane': {'english': 'Crane', 'pronunciation': 'saras'},
        'flamingo': {'english': 'Flamingo', 'pronunciation': 'rajhans'},
        'kingfisher': {'english': 'Kingfisher', 'pronunciation': 'kilkila'},
        'woodpecker': {'english': 'Woodpecker', 'pronunciation': 'kathphodwa'},
        'hummingbird': {'english': 'Hummingbird', 'pronunciation': 'gunjan pakshi'},
        'nightingale': {'english': 'Nightingale', 'pronunciation': 'bulbul'},
        'cuckoo': {'english': 'Cuckoo', 'pronunciation': 'koyal'},
        'mynah': {'english': 'Mynah', 'pronunciation': 'maina'},
        'dove': {'english': 'Dove', 'pronunciation': 'fakhta'},
        'falcon': {'english': 'Falcon', 'pronunciation': 'shaheen'},
        'hawk': {'english': 'Hawk', 'pronunciation': 'baaj'},
        'kite': {'english': 'Kite', 'pronunciation': 'cheel'},
        'turkey': {'english': 'Turkey', 'pronunciation': 'peru'},
        'ostrich': {'english': 'Ostrich', 'pronunciation': 'shutarmurg'},
        'emu': {'english': 'Emu', 'pronunciation': 'emu'},
        'pelican': {'english': 'Pelican', 'pronunciation': 'hawasil'},
        'stork': {'english': 'Stork', 'pronunciation': 'bagula'},
        'heron': {'english': 'Heron', 'pronunciation': 'bagula'}
    },

    # Intermediate Level 3 - Colors
    'colors': {
        'red': {'english': 'Red', 'pronunciation': 'laal'},
        'blue': {'english': 'Blue', 'pronunciation': 'neela'},
        'green': {'english': 'Green', 'pronunciation': 'hara'},
        'yellow': {'english': 'Yellow', 'pronunciation': 'peela'},
        'orange': {'english': 'Orange', 'pronunciation': 'narangi'},
        'purple': {'english': 'Purple', 'pronunciation': 'baingani'},
        'pink': {'english': 'Pink', 'pronunciation': 'gulabi'},
        'black': {'english': 'Black', 'pronunciation': 'kala'},
        'white': {'english': 'White', 'pronunciation': 'safed'},
        'brown': {'english': 'Brown', 'pronunciation': 'bhoora'},
        'gray': {'english': 'Gray', 'pronunciation': 'dhusar'},
        'violet': {'english': 'Violet', 'pronunciation': 'baingani'},
        'indigo': {'english': 'Indigo', 'pronunciation': 'neel'},
        'turquoise': {'english': 'Turquoise', 'pronunciation': 'firoza'},
        'maroon': {'english': 'Maroon', 'pronunciation': 'gehri laal'},
        'navy': {'english': 'Navy', 'pronunciation': 'gehri neeli'},
        'lime': {'english': 'Lime', 'pronunciation': 'chalka hara'},
        'cream': {'english': 'Cream', 'pronunciation': 'malai rang'},
        'beige': {'english': 'Beige', 'pronunciation': 'halka bhoora'},
        'gold': {'english': 'Gold', 'pronunciation': 'sunahara'},
        'silver': {'english': 'Silver', 'pronunciation': 'chandi'},
        'bronze': {'english': 'Bronze', 'pronunciation': 'kansya'}
    },

    # Intermediate Level 4 - Body Parts
    'body_parts': {
        'head': {'english': 'Head', 'pronunciation': 'sir'},
        'hair': {'english': 'Hair', 'pronunciation': 'baal'},
        'face': {'english': 'Face', 'pronunciation': 'chehra'},
        'eye': {'english': 'Eye', 'pronunciation': 'aankh'},
        'nose': {'english': 'Nose', 'pronunciation': 'naak'},
        'ear': {'english': 'Ear', 'pronunciation': 'kaan'},
        'mouth': {'english': 'Mouth', 'pronunciation': 'munh'},
        'teeth': {'english': 'Teeth', 'pronunciation': 'daant'},
        'tongue': {'english': 'Tongue', 'pronunciation': 'jeebh'},
        'neck': {'english': 'Neck', 'pronunciation': 'gardan'},
        'shoulder': {'english': 'Shoulder', 'pronunciation': 'kandha'},
        'arm': {'english': 'Arm', 'pronunciation': 'baaju'},
        'elbow': {'english': 'Elbow', 'pronunciation': 'kuhni'},
        'hand': {'english': 'Hand', 'pronunciation': 'haath'},
        'finger': {'english': 'Finger', 'pronunciation': 'ungli'},
        'thumb': {'english': 'Thumb', 'pronunciation': 'angootha'},
        'chest': {'english': 'Chest', 'pronunciation': 'seena'},
        'back': {'english': 'Back', 'pronunciation': 'peeth'},
        'stomach': {'english': 'Stomach', 'pronunciation': 'pet'},
        'waist': {'english': 'Waist', 'pronunciation': 'kamar'},
        'leg': {'english': 'Leg', 'pronunciation': 'taang'},
        'knee': {'english': 'Knee', 'pronunciation': 'ghutna'},
        'foot': {'english': 'Foot', 'pronunciation': 'paer'},
        'toe': {'english': 'Toe', 'pronunciation': 'paer ki ungli'},
        'heel': {'english': 'Heel', 'pronunciation': 'edi'},
        'forehead': {'english': 'Forehead', 'pronunciation': 'maatha'},
        'eyebrow': {'english': 'Eyebrow', 'pronunciation': 'bhaunh'},
        'eyelash': {'english': 'Eyelash', 'pronunciation': 'palakon ke baal'},
        'cheek': {'english': 'Cheek', 'pronunciation': 'gaal'},
        'chin': {'english': 'Chin', 'pronunciation': 'thodi'},
        'lip': {'english': 'Lip', 'pronunciation': 'honth'},
        'wrist': {'english': 'Wrist', 'pronunciation': 'kalai'},
        'palm': {'english': 'Palm', 'pronunciation': 'hatheli'},
        'nail': {'english': 'Nail', 'pronunciation': 'nakhoon'},
        'ankle': {'english': 'Ankle', 'pronunciation': 'takhna'}
    },

    # Intermediate Level 5 - Family Relations
    'family_relations': {
        'father': {'english': 'Father', 'pronunciation': 'pita'},
        'mother': {'english': 'Mother', 'pronunciation': 'mata'},
        'son': {'english': 'Son', 'pronunciation': 'beta'},
        'daughter': {'english': 'Daughter', 'pronunciation': 'beti'},
        'brother': {'english': 'Brother', 'pronunciation': 'bhai'},
        'sister': {'english': 'Sister', 'pronunciation': 'behen'},
        'grandfather': {'english': 'Grandfather', 'pronunciation': 'dada'},
        'grandmother': {'english': 'Grandmother', 'pronunciation': 'dadi'},
        'uncle': {'english': 'Uncle', 'pronunciation': 'chacha'},
        'aunt': {'english': 'Aunt', 'pronunciation': 'chachi'},
        'cousin': {'english': 'Cousin', 'pronunciation': 'cousin bhai'},
        'nephew': {'english': 'Nephew', 'pronunciation': 'bhatija'},
        'niece': {'english': 'Niece', 'pronunciation': 'bhatiji'},
        'husband': {'english': 'Husband', 'pronunciation': 'pati'},
        'wife': {'english': 'Wife', 'pronunciation': 'patni'},
        'father_in_law': {'english': 'Father-in-law', 'pronunciation': 'sasur'},
        'mother_in_law': {'english': 'Mother-in-law', 'pronunciation': 'saas'},
        'brother_in_law': {'english': 'Brother-in-law', 'pronunciation': 'jija'},
        'sister_in_law': {'english': 'Sister-in-law', 'pronunciation': 'bhabhi'},
        'grandson': {'english': 'Grandson', 'pronunciation': 'pota'},
        'granddaughter': {'english': 'Granddaughter', 'pronunciation': 'poti'},
        'son_in_law': {'english': 'Son-in-law', 'pronunciation': 'damaad'},
        'daughter_in_law': {'english': 'Daughter-in-law', 'pronunciation': 'bahu'},
        'step_father': {'english': 'Step Father', 'pronunciation': 'sautela pita'},
        'step_mother': {'english': 'Step Mother', 'pronunciation': 'sauteli mata'},
        'step_brother': {'english': 'Step Brother', 'pronunciation': 'sautela bhai'},
        'step_sister': {'english': 'Step Sister', 'pronunciation': 'sauteli behen'},
        'maternal_uncle': {'english': 'Maternal Uncle', 'pronunciation': 'mama'},
        'maternal_aunt': {'english': 'Maternal Aunt', 'pronunciation': 'mami'},
        'paternal_uncle': {'english': 'Paternal Uncle', 'pronunciation': 'chacha'},
        'paternal_aunt': {'english': 'Paternal Aunt', 'pronunciation': 'bua'}
    },

    # Common phrases and greetings
    'greetings': {
        'hello': {'english': 'Hello', 'pronunciation': 'namaste'},
        'goodbye': {'english': 'Goodbye', 'pronunciation': 'alvida'},
        'good_morning': {'english': 'Good Morning', 'pronunciation': 'suprabhat'},
        'good_evening': {'english': 'Good Evening', 'pronunciation': 'shubh sandhya'},
        'good_night': {'english': 'Good Night', 'pronunciation': 'shubh ratri'},
        'please': {'english': 'Please', 'pronunciation': 'kripa karke'},
        'thank_you': {'english': 'Thank You', 'pronunciation': 'dhanyawad'},
        'welcome': {'english': 'Welcome', 'pronunciation': 'swagat'},
        'excuse_me': {'english': 'Excuse Me', 'pronunciation': 'maaf kijiye'},
        'sorry': {'english': 'Sorry', 'pronunciation': 'maaf kijiye'},
        'yes': {'english': 'Yes', 'pronunciation': 'haan'},
        'no': {'english': 'No', 'pronunciation': 'nahin'},
        'how_are_you': {'english': 'How are you?', 'pronunciation': 'aap kaise hain?'},
        'i_am_fine': {'english': 'I am fine', 'pronunciation': 'main theek hun'},
        'what_is_your_name': {'english': 'What is your name?', 'pronunciation': 'aapka naam kya hai?'},
        'my_name_is': {'english': 'My name is', 'pronunciation': 'mera naam hai'},
        'nice_to_meet_you': {'english': 'Nice to meet you', 'pronunciation': 'aapse milkar khushi hui'},
        'where_are_you_from': {'english': 'Where are you from?', 'pronunciation': 'aap kahan se hain?'},
        'i_am_from': {'english': 'I am from', 'pronunciation': 'main se hun'},
        'do_you_speak_hindi': {'english': 'Do you speak Hindi?', 'pronunciation': 'kya aap hindi bolte hain?'}
    }
}

def populate_all_vocabulary():
    """Populate database with comprehensive vocabulary and translations"""
    try:
        logger.info("Starting comprehensive vocabulary population...")
        
        # Get translator instance
        translator = get_translator()
        
        # Get database connection
        try:
            db = get_database()
            collection = db.multilingual_vocabulary
            logger.info("Database connection established")
        except Exception as db_error:
            logger.error(f"Database connection failed: {db_error}")
            # Try alternative connection method
            try:
                from mongodb_models import mongo
                db = mongo.db
                collection = db.multilingual_vocabulary
                logger.info("Alternative database connection established")
            except Exception as alt_error:
                logger.error(f"Alternative database connection failed: {alt_error}")
                return False
        
        # Clear existing data
        try:
            collection.delete_many({})
            logger.info("Cleared existing vocabulary data")
        except Exception as clear_error:
            logger.warning(f"Could not clear existing data: {clear_error}")
        
        total_items = 0
        
        for category, items in COMPREHENSIVE_VOCABULARY.items():
            logger.info(f"Processing category: {category} with {len(items)} items")
            
            for key, data in items.items():
                english_text = data['english']
                
                # For now, just store English and basic translation structure
                # We'll implement actual translation in smaller batches to avoid memory issues
                vocab_item = {
                    'category': category,
                    'key': key,
                    'english': english_text,
                    'pronunciation': data.get('pronunciation', ''),
                    'description': data.get('description', ''),
                    'translations': {},  # We'll populate this gradually
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                
                try:
                    collection.insert_one(vocab_item)
                    total_items += 1
                    logger.debug(f"Inserted vocabulary item: {english_text}")
                except Exception as insert_error:
                    logger.warning(f"Failed to insert {english_text}: {insert_error}")
        
        logger.info(f"Successfully populated {total_items} vocabulary items")
        
        # Now try to add some sample translations for testing
        try:
            logger.info("Adding sample translations...")
            sample_items = collection.find().limit(5)
            
            for item in sample_items:
                translations = {}
                english_text = item['english']
                
                # Test translation for a few key languages
                test_languages = ['hindi', 'tamil', 'bengali']
                
                for lang in test_languages:
                    try:
                        translation = translator.translate_text(english_text, lang)
                        translations[lang] = translation
                        logger.debug(f"Translated '{english_text}' to {lang}: '{translation}'")
                    except Exception as trans_error:
                        logger.warning(f"Failed to translate '{english_text}' to {lang}: {trans_error}")
                        translations[lang] = english_text  # Fallback
                
                # Update the item with translations
                collection.update_one(
                    {'_id': item['_id']},
                    {'$set': {'translations': translations}}
                )
            
            logger.info("Sample translations added successfully")
            
        except Exception as trans_error:
            logger.warning(f"Sample translation process failed: {trans_error}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to populate vocabulary: {e}")
        return False

def get_vocabulary_for_level(level, language='english'):
    """Get vocabulary data for a specific level in specified language"""
    try:
        level_mapping = {
            'beginner': ['hindi_vowels', 'hindi_consonants', 'greetings'],
            'intermediate_1': ['fruits', 'vegetables'],
            'intermediate_2': ['animals', 'birds'],
            'intermediate_3': ['colors'],
            'intermediate_4': ['body_parts'],
            'intermediate_5': ['family_relations'],
        }
        
        categories = level_mapping.get(level, [])
        vocabulary = {}
        
        for category in categories:
            vocab_items = MultilingualVocabulary.get_vocabulary_by_category(category, language)
            vocabulary[category] = vocab_items
        
        return vocabulary
        
    except Exception as e:
        logger.error(f"Failed to get vocabulary for level {level}: {e}")
        return {}

def translate_level_content(level_content, target_language):
    """Translate level content (titles, instructions, etc.) to target language"""
    try:
        translator = get_translator()
        
        translated_content = {}
        for key, text in level_content.items():
            if isinstance(text, str):
                translated_content[key] = translator.translate_text(text, target_language)
            else:
                translated_content[key] = text
        
        return translated_content
        
    except Exception as e:
        logger.error(f"Failed to translate level content: {e}")
        return level_content

if __name__ == "__main__":
    from datetime import datetime
    # Test the vocabulary population
    print("Testing comprehensive vocabulary population...")
    result = populate_all_vocabulary()
    if result:
        print("✅ Vocabulary populated successfully!")
    else:
        print("❌ Failed to populate vocabulary")