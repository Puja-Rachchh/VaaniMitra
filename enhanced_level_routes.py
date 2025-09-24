"""
Enhanced routes for all learning levels with translation support
Supports English to any Indian language for beginner and intermediate levels
"""
from flask import render_template, request, session, redirect, url_for, jsonify
from translation_service import get_translator
from comprehensive_vocabulary import get_vocabulary_for_level, translate_level_content
from mongodb_models import UserProgress, get_database
from datetime import datetime
import logging
import random

logger = logging.getLogger(__name__)

# Level content that needs translation
LEVEL_CONTENT = {
    'beginner': {
        'title': 'Choose Your Learning Path',
        'learn_letters_title': 'Learn Letters',
        'learn_letters_desc': 'Start with basic Hindi letters and their pronunciations',
        'take_quiz_title': 'Take Quiz',
        'take_quiz_desc': 'Test your knowledge of Hindi letters'
    },
    'intermediate': {
        'title': 'Intermediate Hindi Levels',
        'level_1': {
            'title': 'Fruits and Vegetables',
            'description': 'Learn Hindi names for common fruits and vegetables with pronunciation.',
            'quiz_instruction': 'Match the Hindi word with its English meaning'
        },
        'level_2': {
            'title': 'Animals and Birds',
            'description': 'Learn Hindi names for common animals and birds with pronunciation and images.',
            'quiz_instruction': 'Choose the correct Hindi name for the animal shown'
        },
        'level_3': {
            'title': 'Colors',
            'description': 'Learn Hindi names for different colors with pronunciation and examples.',
            'quiz_instruction': 'Select the correct Hindi word for the color shown'
        },
        'level_4': {
            'title': 'Body Parts',
            'description': 'Learn Hindi names for body parts with pronunciation and images.',
            'quiz_instruction': 'Identify the correct Hindi name for the body part'
        },
        'level_5': {
            'title': 'Family Relations',
            'description': 'Learn Hindi names for family relations with pronunciation and images.',
            'quiz_instruction': 'Match the family relation with its Hindi equivalent'
        }
    }
}

@app.route('/api/translate-content')
def translate_content():
    """API endpoint to translate level content"""
    try:
        level = request.args.get('level', 'beginner')
        language = request.args.get('language', 'english')
        
        if language == 'english':
            return jsonify(LEVEL_CONTENT.get(level, {}))
        
        translator = get_translator()
        content = LEVEL_CONTENT.get(level, {})
        translated_content = translator.translate_level_content(content, language)
        
        return jsonify(translated_content)
    
    except Exception as e:
        logger.error(f"Error translating content: {e}")
        return jsonify({'error': 'Translation failed'}), 500

@app.route('/api/level-vocabulary/<level>')
def get_level_vocabulary_api(level):
    """API endpoint to get vocabulary for a specific level"""
    try:
        language = request.args.get('language', 'english')
        vocabulary = get_vocabulary_for_level(level, language)
        return jsonify(vocabulary)
    
    except Exception as e:
        logger.error(f"Error getting vocabulary: {e}")
        return jsonify({'error': 'Failed to get vocabulary'}), 500

@app.route('/beginner')
def beginner_choice():
    """Enhanced beginner choice page with language support"""
    return render_template('beginner_choice.html')

@app.route('/intermediate')
def intermediate_levels():
    """Enhanced intermediate levels page with language support"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Get user progress
    try:
        db = get_database()
        progress_collection = db.user_progress
        
        progress = progress_collection.find_one({'user_id': user_id})
        
        if not progress:
            # Create initial progress
            initial_progress = {
                'user_id': user_id,
                'intermediate_level1_score': 0,
                'intermediate_level2_score': 0,
                'intermediate_level3_score': 0,
                'intermediate_level4_score': 0,
                'intermediate_level5_score': 0,
                'passed_level1': False,
                'passed_level2': False,
                'passed_level3': False,
                'passed_level4': False,
                'passed_level5': False
            }
            progress_collection.insert_one(initial_progress)
            progress = initial_progress
        
        return render_template('intermediate_levels.html',
                             score1=progress.get('intermediate_level1_score', 0),
                             score2=progress.get('intermediate_level2_score', 0),
                             score3=progress.get('intermediate_level3_score', 0),
                             score4=progress.get('intermediate_level4_score', 0),
                             score5=progress.get('intermediate_level5_score', 0),
                             passed_level1=progress.get('passed_level1', False),
                             passed_level2=progress.get('passed_level2', False),
                             passed_level3=progress.get('passed_level3', False),
                             passed_level4=progress.get('passed_level4', False),
                             passed_level5=progress.get('passed_level5', False))
    
    except Exception as e:
        logger.error(f"Error getting user progress: {e}")
        return render_template('intermediate_levels.html')

@app.route('/intermediate/<int:level>')
def intermediate_level(level):
    """Enhanced intermediate level pages with translation support"""
    if level not in [1, 2, 3, 4, 5]:
        return redirect(url_for('intermediate_levels'))
    
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Check if level is unlocked
    user_id = session['user_id']
    db = get_database()
    progress_collection = db.user_progress
    progress = progress_collection.find_one({'user_id': user_id})
    
    if not progress:
        return redirect(url_for('intermediate_levels'))
    
    # Check unlock conditions
    if level > 1:
        previous_level_passed = progress.get(f'passed_level{level-1}', False)
        if not previous_level_passed:
            return redirect(url_for('intermediate_levels'))
    
    # Get vocabulary for this level
    level_mapping = {
        1: 'intermediate_1',
        2: 'intermediate_2',
        3: 'intermediate_3',
        4: 'intermediate_4',
        5: 'intermediate_5'
    }
    
    level_key = level_mapping[level]
    vocabulary = get_vocabulary_for_level(level_key, 'english')
    
    template_name = f'intermediate_level{level}.html'
    return render_template(template_name, vocabulary=vocabulary, level=level)

@app.route('/intermediate/<int:level>/quiz')
def intermediate_level_quiz(level):
    """Enhanced intermediate level quiz with translation support"""
    if level not in [1, 2, 3, 4, 5]:
        return redirect(url_for('intermediate_levels'))
    
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Generate quiz questions based on level
    level_mapping = {
        1: 'intermediate_1',
        2: 'intermediate_2',
        3: 'intermediate_3',
        4: 'intermediate_4',
        5: 'intermediate_5'
    }
    
    level_key = level_mapping[level]
    vocabulary = get_vocabulary_for_level(level_key, 'english')
    
    # Generate random quiz questions
    questions = generate_quiz_questions(vocabulary, level)
    
    template_name = f'intermediate_level{level}_quiz.html'
    return render_template(template_name, questions=questions, level=level)

def generate_quiz_questions(vocabulary, level, num_questions=5):
    """Generate quiz questions from vocabulary"""
    try:
        questions = []
        
        # Collect all vocabulary items
        all_items = []
        for category, items in vocabulary.items():
            for key, data in items.items():
                all_items.append({
                    'english': data.get('english', key),
                    'hindi': data.get('pronunciation', ''),
                    'category': category
                })
        
        if len(all_items) < num_questions:
            num_questions = len(all_items)
        
        # Select random items for questions
        selected_items = random.sample(all_items, num_questions)
        
        for i, item in enumerate(selected_items):
            # Create multiple choice options
            wrong_options = random.sample(
                [x for x in all_items if x != item], 
                min(3, len(all_items) - 1)
            )
            
            options = [item['english']] + [x['english'] for x in wrong_options]
            random.shuffle(options)
            
            question = {
                'id': i + 1,
                'question': f"What is the English meaning of '{item['hindi']}'?",
                'options': options,
                'correct_answer': item['english'],
                'category': item['category']
            }
            questions.append(question)
        
        return questions
    
    except Exception as e:
        logger.error(f"Error generating quiz questions: {e}")
        return []

@app.route('/api/translate-quiz')
def translate_quiz():
    """API endpoint to translate quiz questions"""
    try:
        level = request.args.get('level', '1')
        language = request.args.get('language', 'english')
        
        if language == 'english':
            return jsonify({'success': True, 'message': 'No translation needed'})
        
        # Get quiz questions
        level_mapping = {
            '1': 'intermediate_1',
            '2': 'intermediate_2',
            '3': 'intermediate_3',
            '4': 'intermediate_4',
            '5': 'intermediate_5'
        }
        
        level_key = level_mapping.get(level, 'intermediate_1')
        vocabulary = get_vocabulary_for_level(level_key, 'english')
        questions = generate_quiz_questions(vocabulary, int(level))
        
        # Translate questions
        translator = get_translator()
        translated_questions = translator.translate_quiz_questions(questions, language)
        
        return jsonify({
            'success': True,
            'questions': translated_questions
        })
    
    except Exception as e:
        logger.error(f"Error translating quiz: {e}")
        return jsonify({'error': 'Translation failed'}), 500

@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    """Enhanced quiz submission with progress tracking"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        data = request.get_json()
        level = data.get('level')
        answers = data.get('answers', {})
        
        # Calculate score
        total_questions = len(answers)
        correct_answers = sum(1 for answer in answers.values() if answer.get('correct', False))
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Update user progress
        user_id = session['user_id']
        db = get_database()
        progress_collection = db.user_progress
        
        update_data = {
            f'intermediate_level{level}_score': score,
            f'passed_level{level}': score >= 60  # 60% to pass
        }
        
        progress_collection.update_one(
            {'user_id': user_id},
            {'$set': update_data},
            upsert=True
        )
        
        return jsonify({
            'success': True,
            'score': score,
            'correct': correct_answers,
            'total': total_questions,
            'passed': score >= 60
        })
    
    except Exception as e:
        logger.error(f"Error submitting quiz: {e}")
        return jsonify({'error': 'Failed to submit quiz'}), 500

# Language support API
@app.route('/api/supported-languages')
def get_supported_languages():
    """Get list of supported languages"""
    try:
        translator = get_translator()
        languages = translator.get_available_languages()
        
        # Language display names
        language_names = {
            'english': 'English',
            'hindi': 'हिंदी',
            'bengali': 'বাংলা',
            'tamil': 'தமிழ்',
            'telugu': 'తెలుగు',
            'marathi': 'मराठी',
            'gujarati': 'ગુજરાતી',
            'kannada': 'ಕನ್ನಡ',
            'malayalam': 'മലയാളം',
            'punjabi': 'ਪੰਜਾਬੀ',
            'urdu': 'اردو',
            'assamese': 'অসমীয়া',
            'odia': 'ଓଡ଼ିଆ',
            'nepali': 'नेपाली',
            'sindhi': 'سنڌي'
        }
        
        return jsonify({
            'languages': languages,
            'display_names': language_names
        })
    
    except Exception as e:
        logger.error(f"Error getting supported languages: {e}")
        return jsonify({'error': 'Failed to get languages'}), 500

# User language preference
@app.route('/api/user-language', methods=['GET', 'POST'])
def user_language_preference():
    """Get or set user language preference"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        user_id = session['user_id']
        db = get_database()
        preferences_collection = db.user_language_preferences
        
        if request.method == 'POST':
            # Set language preference
            data = request.get_json()
            language = data.get('language', 'english')
            
            preferences_collection.update_one(
                {'user_id': user_id},
                {'$set': {'preferred_language': language, 'updated_at': datetime.utcnow()}},
                upsert=True
            )
            
            return jsonify({'success': True, 'language': language})
        
        else:
            # Get language preference
            preference = preferences_collection.find_one({'user_id': user_id})
            language = preference.get('preferred_language', 'english') if preference else 'english'
            return jsonify({'language': language})
    
    except Exception as e:
        logger.error(f"Error handling user language preference: {e}")
        return jsonify({'error': 'Failed to handle language preference'}), 500