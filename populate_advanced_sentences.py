"""
Populate Advanced Level Sentence Translations
Adds translations for all advanced level sentences to MongoDB
"""

from mongodb_models import mongo
from native_content_system import get_advanced_sentences, get_all_sentence_categories
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Manual translations for advanced level sentences
SENTENCE_TRANSLATIONS = {
    'hindi': {
        # Greetings
        'hello, how are you?': 'नमस्ते, आप कैसे हैं?',
        'good morning, have a nice day.': 'सुप्रभात, आपका दिन शुभ हो।',
        'nice to meet you.': 'आपसे मिलकर अच्छा लगा।',
        'how is your family?': 'आपका परिवार कैसा है?',
        'thank you very much.': 'बहुत धन्यवाद।',
        
        # Introductions
        'my name is john.': 'मेरा नाम जॉन है।',
        'i am a student.': 'मैं एक छात्र हूं।',
        'i live in mumbai.': 'मैं मुंबई में रहता हूं।',
        'i am learning hindi.': 'मैं हिंदी सीख रहा हूं।',
        'this is my family.': 'यह मेरा परिवार है।',
        
        # Daily Activities
        "i wake up at six o'clock.": 'मैं छह बजे उठता हूं।',
        'i eat breakfast in the morning.': 'मैं सुबह नाश्ता करता हूं।',
        'i go to school by bus.': 'मैं बस से स्कूल जाता हूं।',
        'i study every day.': 'मैं हर दिन पढ़ता हूं।',
        'i sleep at night.': 'मैं रात को सोता हूं।',
        
        # Questions
        'what is your name?': 'आपका नाम क्या है?',
        'where do you live?': 'आप कहां रहते हैं?',
        'how old are you?': 'आपकी उम्र क्या है?',
        'what time is it?': 'क्या समय है?',
        'do you speak english?': 'क्या आप अंग्रेजी बोलते हैं?',
        
        # Shopping
        'how much does this cost?': 'यह कितने का है?',
        'i want to buy this.': 'मैं यह खरीदना चाहता हूं।',
        'do you have a smaller size?': 'क्या आपके पास छोटा साइज है?',
        'can i pay by card?': 'क्या मैं कार्ड से भुगतान कर सकता हूं?',
        'please give me a bag.': 'कृपया मुझे एक थैला दें।',
        
        # Directions
        'where is the railway station?': 'रेलवे स्टेशन कहां है?',
        'how do i get to the market?': 'मैं बाजार कैसे जाऊं?',
        'is it far from here?': 'क्या यह यहां से दूर है?',
        'please turn left.': 'कृपया बाएं मुड़ें।',
        'go straight ahead.': 'सीधे आगे जाएं।'
    },
    
    'gujarati': {
        # Greetings
        'hello, how are you?': 'નમસ્તે, તમે કેમ છો?',
        'good morning, have a nice day.': 'સુપ્રભાત, તમારો દિવસ સારો જાય.',
        'nice to meet you.': 'તમને મળીને આનંદ થયો.',
        'how is your family?': 'તમારો પરિવાર કેવો છે?',
        'thank you very much.': 'ખૂબ ખૂબ આભાર.',
        
        # Introductions
        'my name is john.': 'મારું નામ જોન છે.',
        'i am a student.': 'હું એક વિદ્યાર્થી છું.',
        'i live in mumbai.': 'હું મુંબઈમાં રહું છું.',
        'i am learning hindi.': 'હું હિન્દી શીખી રહ્યો છું.',
        'this is my family.': 'આ મારો પરિવાર છે.',
        
        # Daily Activities
        "i wake up at six o'clock.": 'હું છ વાગ્યે જાગું છું.',
        'i eat breakfast in the morning.': 'હું સવારે નાસ્તો કરું છું.',
        'i go to school by bus.': 'હું બસથી શાળાએ જાઉં છું.',
        'i study every day.': 'હું દરરોજ અભ્યાસ કરું છું.',
        'i sleep at night.': 'હું રાત્રે સૂઈ જાઉં છું.',
        
        # Questions
        'what is your name?': 'તમારું નામ શું છે?',
        'where do you live?': 'તમે ક્યાં રહો છો?',
        'how old are you?': 'તમારી ઉંમર શું છે?',
        'what time is it?': 'શું સમય છે?',
        'do you speak english?': 'શું તમે અંગ્રેજી બોલો છો?',
        
        # Shopping
        'how much does this cost?': 'આ કેટલાનું છે?',
        'i want to buy this.': 'હું આ ખરીદવા માંગું છું.',
        'do you have a smaller size?': 'શું તમારી પાસે નાનું સાઈઝ છે?',
        'can i pay by card?': 'શું હું કાર્ડથી ચૂકવણી કરી શકું?',
        'please give me a bag.': 'કૃપા કરીને મને બેગ આપો.',
        
        # Directions
        'where is the railway station?': 'રેલવે સ્ટેશન ક્યાં છે?',
        'how do i get to the market?': 'હું બજારમાં કેવી રીતે જાઉં?',
        'is it far from here?': 'શું તે અહીંથી દૂર છે?',
        'please turn left.': 'કૃપા કરીને ડાબી બાજુ વળો.',
        'go straight ahead.': 'સીધા આગળ જાઓ.'
    },
    
    'tamil': {
        # Greetings
        'hello, how are you?': 'வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?',
        'good morning, have a nice day.': 'காலை வணக்கம், உங்கள் நாள் இனிமையாக இருக்கட்டும்.',
        'nice to meet you.': 'உங்களை சந்தித்ததில் மகிழ்ச்சி.',
        'how is your family?': 'உங்கள் குடும்பம் எப்படி இருக்கிறது?',
        'thank you very much.': 'மிக்க நன்றி.',
        
        # Introductions
        'my name is john.': 'என் பெயர் ஜான்.',
        'i am a student.': 'நான் ஒரு மாணவன்.',
        'i live in mumbai.': 'நான் மும்பையில் வசிக்கிறேன்.',
        'i am learning hindi.': 'நான் இந்தி கற்றுக்கொண்டிருக்கிறேன்.',
        'this is my family.': 'இது என் குடும்பம்.',
        
        # Daily Activities
        "i wake up at six o'clock.": 'நான் ஆறு மணிக்கு எழுவேன்.',
        'i eat breakfast in the morning.': 'நான் காலையில் காலை உணவு சாப்பிடுகிறேன்.',
        'i go to school by bus.': 'நான் பேருந்தில் பள்ளிக்கு செல்கிறேன்.',
        'i study every day.': 'நான் தினமும் படிக்கிறேன்.',
        'i sleep at night.': 'நான் இரவில் தூங்குகிறேன்.',
        
        # Questions
        'what is your name?': 'உங்கள் பெயர் என்ன?',
        'where do you live?': 'நீங்கள் எங்கே வசிக்கிறீர்கள்?',
        'how old are you?': 'உங்கள் வயது என்ன?',
        'what time is it?': 'என்ன நேரம்?',
        'do you speak english?': 'நீங்கள் ஆங்கிலம் பேசுகிறீர்களா?',
        
        # Shopping
        'how much does this cost?': 'இதன் விலை என்ன?',
        'i want to buy this.': 'நான் இதை வாங்க விரும்புகிறேன்.',
        'do you have a smaller size?': 'உங்களிடம் சிறிய அளவு உள்ளதா?',
        'can i pay by card?': 'நான் கார்டு மூலம் பணம் செலுத்தலாமா?',
        'please give me a bag.': 'தயவுசெய்து எனக்கு ஒரு பை கொடுங்கள்.',
        
        # Directions
        'where is the railway station?': 'ரயில் நிலையம் எங்கே?',
        'how do i get to the market?': 'நான் சந்தைக்கு எப்படி செல்வது?',
        'is it far from here?': 'இது இங்கிருந்து தூரமா?',
        'please turn left.': 'தயவுசெய்து இடதுபுறம் திரும்புங்கள்.',
        'go straight ahead.': 'நேராக முன்னால் செல்லுங்கள்.'
    },
    
    'bengali': {
        # Greetings
        'hello, how are you?': 'নমস্কার, আপনি কেমন আছেন?',
        'good morning, have a nice day.': 'সুপ্রভাত, আপনার দিনটি ভালো কাটুক।',
        'nice to meet you.': 'আপনার সাথে দেখা করে ভালো লাগলো।',
        'how is your family?': 'আপনার পরিবার কেমন আছে?',
        'thank you very much.': 'আপনাকে অনেক ধন্যবাদ।',
        
        # Introductions
        'my name is john.': 'আমার নাম জন।',
        'i am a student.': 'আমি একজন ছাত্র।',
        'i live in mumbai.': 'আমি মুম্বাইতে থাকি।',
        'i am learning hindi.': 'আমি হিন্দি শিখছি।',
        'this is my family.': 'এটি আমার পরিবার।',
        
        # Daily Activities
        "i wake up at six o'clock.": 'আমি ছয়টায় ঘুম থেকে উঠি।',
        'i eat breakfast in the morning.': 'আমি সকালে নাস্তা করি।',
        'i go to school by bus.': 'আমি বাসে স্কুলে যাই।',
        'i study every day.': 'আমি প্রতিদিন পড়াশোনা করি।',
        'i sleep at night.': 'আমি রাতে ঘুমাই।',
        
        # Questions
        'what is your name?': 'আপনার নাম কি?',
        'where do you live?': 'আপনি কোথায় থাকেন?',
        'how old are you?': 'আপনার বয়স কত?',
        'what time is it?': 'এখন কয়টা বাজে?',
        'do you speak english?': 'আপনি কি ইংরেজি বলেন?',
        
        # Shopping
        'how much does this cost?': 'এটির দাম কত?',
        'i want to buy this.': 'আমি এটি কিনতে চাই।',
        'do you have a smaller size?': 'আপনার কাছে কি ছোট সাইজ আছে?',
        'can i pay by card?': 'আমি কি কার্ড দিয়ে পেমেন্ট করতে পারি?',
        'please give me a bag.': 'দয়া করে আমাকে একটি ব্যাগ দিন।',
        
        # Directions
        'where is the railway station?': 'রেলওয়ে স্টেশন কোথায়?',
        'how do i get to the market?': 'আমি বাজারে কিভাবে যাব?',
        'is it far from here?': 'এটি কি এখান থেকে দূরে?',
        'please turn left.': 'দয়া করে বামদিকে ঘুরুন।',
        'go straight ahead.': 'সোজা সামনে যান।'
    },
    
    'telugu': {
        # Greetings
        'hello, how are you?': 'నమస్కారం, మీరు ఎలా ఉన్నారు?',
        'good morning, have a nice day.': 'శుభోదయం, మీ రోజు శుభంగా ఉండాలి.',
        'nice to meet you.': 'మిమ్మల్ని కలవడం ఆనందంగా ఉంది.',
        'how is your family?': 'మీ కుటుంబం ఎలా ఉంది?',
        'thank you very much.': 'చాలా ధన్యవాదాలు.',
        
        # Introductions
        'my name is john.': 'నా పేరు జాన్.',
        'i am a student.': 'నేను విద్యార్థిని.',
        'i live in mumbai.': 'నేను ముంబైలో నివసిస్తున్నాను.',
        'i am learning hindi.': 'నేను హిందీ నేర్చుకుంటున్నాను.',
        'this is my family.': 'ఇది నా కుటుంబం.',
        
        # Daily Activities
        "i wake up at six o'clock.": 'నేను ఆరు గంటలకు మేల్కొంటాను.',
        'i eat breakfast in the morning.': 'నేను ఉదయం అల్పాహారం తింటాను.',
        'i go to school by bus.': 'నేను బస్సులో పాఠశాలకు వెళ్తాను.',
        'i study every day.': 'నేను ప్రతిరోజు చదువుతాను.',
        'i sleep at night.': 'నేను రాత్రి పడుకుంటాను.',
        
        # Questions
        'what is your name?': 'మీ పేరు ఏమిటి?',
        'where do you live?': 'మీరు ఎక్కడ నివసిస్తున్నారు?',
        'how old are you?': 'మీ వయస్సు ఎంత?',
        'what time is it?': 'సమయం ఎంత?',
        'do you speak english?': 'మీరు ఆంగ్లం మాట్లాడతారా?',
        
        # Shopping
        'how much does this cost?': 'దీని ఖరీదు ఎంత?',
        'i want to buy this.': 'నేను దీన్ని కొనాలనుకుంటున్నాను.',
        'do you have a smaller size?': 'మీ వద్ద చిన్న పరిమాణం ఉందా?',
        'can i pay by card?': 'నేను కార్డు ద్వారా చెల్లించవచ్చా?',
        'please give me a bag.': 'దయచేసి నాకు ఒక సంచి ఇవ్వండి.',
        
        # Directions
        'where is the railway station?': 'రైల్వే స్టేషన్ ఎక్కడ ఉంది?',
        'how do i get to the market?': 'నేను మార్కెట్‌కు ఎలా వెళ్లాలి?',
        'is it far from here?': 'ఇది ఇక్కడ నుండి దూరంగా ఉందా?',
        'please turn left.': 'దయచేసి ఎడమవైపు తిరగండి.',
        'go straight ahead.': 'నేరుగా ముందుకు వెళ్ళండి.'
    }
}

def populate_advanced_sentences():
    """Populate database with advanced level sentence translations"""
    try:
        total_added = 0
        total_updated = 0
        
        for language, sentences in SENTENCE_TRANSLATIONS.items():
            logger.info(f"\nProcessing {language} sentences...")
            
            for english_text, translation in sentences.items():
                try:
                    # Check if translation exists
                    existing = mongo.db.translations.find_one({
                        'english': english_text.lower(),
                        'language': language.lower()
                    })
                    
                    translation_doc = {
                        'english': english_text.lower(),
                        'language': language.lower(),
                        'translation': translation,
                        'category': 'sentences',
                        'updated_at': datetime.utcnow()
                    }
                    
                    if existing:
                        # Update existing
                        mongo.db.translations.update_one(
                            {'_id': existing['_id']},
                            {'$set': translation_doc}
                        )
                        total_updated += 1
                        logger.info(f"  Updated: '{english_text}' -> '{translation}'")
                    else:
                        # Insert new
                        translation_doc['created_at'] = datetime.utcnow()
                        mongo.db.translations.insert_one(translation_doc)
                        total_added += 1
                        logger.info(f"  Added: '{english_text}' -> '{translation}'")
                        
                except Exception as e:
                    logger.error(f"  Error processing '{english_text}': {e}")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Population complete!")
        logger.info(f"Total added: {total_added}")
        logger.info(f"Total updated: {total_updated}")
        logger.info(f"{'='*60}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error populating advanced sentences: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    from app import app
    
    with app.app_context():
        logger.info("Starting advanced level sentence population...")
        success = populate_advanced_sentences()
        
        if success:
            logger.info("\n✓ Successfully populated advanced level sentences!")
        else:
            logger.error("\n✗ Failed to populate advanced level sentences")
