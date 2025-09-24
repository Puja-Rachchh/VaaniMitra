"""
Translation routes for VaaniMitra
Handle language switching and translation services
"""

from flask import request, jsonify, session
from app import app
from mongodb_models import MultilingualVocabulary, UserLanguagePreference
from translation_service import get_translator, translate_vocabulary_data
import logging

logger = logging.getLogger(__name__)

@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    try:
        translator = get_translator()
        languages = translator.get_available_languages()
        
        # Add display names for languages
        language_display = {
            'english': 'English',
            'hindi': 'हिंदी (Hindi)',
            'bengali': 'বাংলা (Bengali)', 
            'gujarati': 'ગુજરાતી (Gujarati)',
            'kannada': 'ಕನ್ನಡ (Kannada)',
            'malayalam': 'മലയാളം (Malayalam)',
            'marathi': 'मराठी (Marathi)',
            'oriya': 'ଓଡ଼ିଆ (Oriya)',
            'punjabi': 'ਪੰਜਾਬੀ (Punjabi)',
            'tamil': 'தமிழ் (Tamil)',
            'telugu': 'తెలుగు (Telugu)',
            'urdu': 'اردو (Urdu)',
            'assamese': 'অসমীয়া (Assamese)',
            'nepali': 'नेपाली (Nepali)',
            'sanskrit': 'संस्कृत (Sanskrit)'
        }
        
        formatted_languages = []
        for lang in languages:
            formatted_languages.append({
                'code': lang,
                'name': language_display.get(lang, lang.title()),
                'native_name': language_display.get(lang, lang.title())
            })
        
        return jsonify({
            'success': True,
            'languages': formatted_languages
        })
    except Exception as e:
        logger.error(f"Error getting supported languages: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get supported languages'
        }), 500

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text to specified language"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        target_language = data.get('target_language', 'hindi')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        translator = get_translator()
        translation = translator.translate_text(text, target_language)
        
        return jsonify({
            'success': True,
            'original': text,
            'translation': translation,
            'target_language': target_language
        })
    
    except Exception as e:
        logger.error(f"Error translating text: {e}")
        return jsonify({
            'success': False,
            'error': 'Translation failed'
        }), 500

@app.route('/api/vocabulary/<category>', methods=['GET'])
def get_vocabulary_category(category):
    """Get vocabulary for a specific category in user's preferred language"""
    try:
        # Get user's preferred language from session or default to Hindi
        preferred_language = session.get('preferred_language', 'hindi')
        
        # Override with query parameter if provided
        language = request.args.get('language', preferred_language)
        
        vocabulary = MultilingualVocabulary.get_vocabulary_by_category(category, language)
        
        return jsonify({
            'success': True,
            'category': category,
            'language': language,
            'vocabulary': vocabulary
        })
    
    except Exception as e:
        logger.error(f"Error getting vocabulary for category {category}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get vocabulary'
        }), 500

@app.route('/api/vocabulary/categories', methods=['GET'])
def get_vocabulary_categories():
    """Get all available vocabulary categories"""
    try:
        categories = MultilingualVocabulary.get_all_categories()
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        logger.error(f"Error getting vocabulary categories: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get categories'
        }), 500

@app.route('/api/user/language-preference', methods=['GET', 'POST'])
def user_language_preference():
    """Get or set user language preferences"""
    try:
        user_id = session.get('user_id')
        
        if request.method == 'GET':
            if user_id:
                preferences = UserLanguagePreference.get_user_preferences(user_id)
                if preferences:
                    return jsonify({
                        'success': True,
                        'preferred_language': preferences.preferred_language,
                        'native_language': preferences.native_language,
                        'learning_languages': preferences.learning_languages
                    })
            
            # Return default preferences
            return jsonify({
                'success': True,
                'preferred_language': session.get('preferred_language', 'hindi'),
                'native_language': 'english',
                'learning_languages': []
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            preferred_language = data.get('preferred_language', 'hindi')
            native_language = data.get('native_language', 'english')
            learning_languages = data.get('learning_languages', [])
            
            # Store in session for immediate use
            session['preferred_language'] = preferred_language
            
            # Store in database if user is logged in
            if user_id:
                preferences = UserLanguagePreference.get_user_preferences(user_id)
                if not preferences:
                    preferences = UserLanguagePreference(user_id=user_id)
                
                preferences.preferred_language = preferred_language
                preferences.native_language = native_language
                preferences.learning_languages = learning_languages
                preferences.save()
            
            return jsonify({
                'success': True,
                'message': 'Language preferences updated'
            })
    
    except Exception as e:
        logger.error(f"Error handling language preferences: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to handle language preferences'
        }), 500

@app.route('/api/admin/populate-vocabulary', methods=['POST'])
def populate_vocabulary():
    """Admin route to populate vocabulary with translations"""
    try:
        # This should be restricted to admin users in production
        result = translate_vocabulary_data()
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Vocabulary populated successfully with translations'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to populate vocabulary'
            }), 500
    
    except Exception as e:
        logger.error(f"Error populating vocabulary: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to populate vocabulary'
        }), 500

@app.route('/api/vocabulary/search', methods=['GET'])
def search_vocabulary():
    """Search vocabulary across all categories"""
    try:
        query = request.args.get('q', '').strip()
        language = request.args.get('language', session.get('preferred_language', 'hindi'))
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        # Simple search implementation - can be enhanced with MongoDB text search
        categories = MultilingualVocabulary.get_all_categories()
        results = []
        
        for category in categories:
            vocabulary = MultilingualVocabulary.get_vocabulary_by_category(category, language)
            for item in vocabulary:
                if (query.lower() in item['english'].lower() or 
                    query.lower() in item['translation'].lower()):
                    results.append(item)
        
        return jsonify({
            'success': True,
            'query': query,
            'language': language,
            'results': results[:50]  # Limit to 50 results
        })
    
    except Exception as e:
        logger.error(f"Error searching vocabulary: {e}")
        return jsonify({
            'success': False,
            'error': 'Search failed'
        }), 500

@app.route('/api/vocabulary/item/<category>/<key>', methods=['GET'])
def get_vocabulary_item(category, key):
    """Get a specific vocabulary item with all translations"""
    try:
        vocab_item = MultilingualVocabulary.find_by_key(category, key)
        
        if not vocab_item:
            return jsonify({
                'success': False,
                'error': 'Vocabulary item not found'
            }), 404
        
        return jsonify({
            'success': True,
            'category': vocab_item.category,
            'key': vocab_item.key,
            'english': vocab_item.english,
            'translations': vocab_item.translations
        })
    
    except Exception as e:
        logger.error(f"Error getting vocabulary item {category}/{key}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get vocabulary item'
        }), 500