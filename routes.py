from flask import render_template, request, redirect, url_for, session, jsonify, send_file, after_this_request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from mongodb_models import User, UserProgress, mongo
from app import app, login_manager
from native_content_system import get_language_letters, get_english_vocabulary, get_all_vocabulary_categories
from indictrans2_service import translation_service
import os
import random
from gtts import gTTS

@app.route('/')
def index():
    # Clear any invalid session data
    if 'user' in session:
        user = User.find_by_username(session['user'])
        if user:
            return redirect(url_for('home'))
        else:
            # Clear invalid session
            session.clear()
    return render_template('index.html')

@app.route('/home')
def home():
    if 'user' in session:
        user = User.find_by_username(session['user'])
        if user:
            return render_template('index.html', username=user.username, known=user.known_language, target=user.target_language, level=user.level)
    return redirect(url_for('login'))

@app.route('/language_letters')
def language_letters():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.find_by_username(session['user'])
    if not user or not user.target_language or user.level != 'beginner':
        return redirect(url_for('home'))
    
    # Get letters for the user's target language
    letters_dict = get_language_letters(user.target_language)
    
    # Convert dictionary format to list format for template
    letters = {}
    if letters_dict:
        # Convert vowels dict to list
        if 'vowels' in letters_dict:
            letters['vowels'] = []
            for key, data in letters_dict['vowels'].items():
                letters['vowels'].append({
                    'letter': data['letter'],
                    'name': data['pronunciation'],
                    'romanization': data.get('transliteration', '')
                })
        
        # Convert consonants dict to list  
        if 'consonants' in letters_dict:
            letters['consonants'] = []
            for key, data in letters_dict['consonants'].items():
                letters['consonants'].append({
                    'letter': data['letter'],
                    'name': data['pronunciation'],
                    'romanization': data.get('transliteration', '')
                })
    
    # Calculate total letters count
    total_letters = 0
    if letters:
        total_letters += len(letters.get('vowels', []))
        total_letters += len(letters.get('consonants', []))
    
    return render_template('language_letters.html', 
                         letters=letters, 
                         target_language=user.target_language,
                         known_language=user.known_language,
                         total_letters=total_letters)

@app.route('/play_letter', methods=['POST'])
def play_letter():
    print("=== PLAY_LETTER ROUTE CALLED ===")
    if 'user' not in session:
        print("ERROR: User not authenticated")
        return jsonify({'error': 'Not authenticated'}), 401
    
    print(f"User in session: {session.get('user')}")
    data = request.get_json()
    print(f"Received data: {data}")
    
    letter = data.get('letter')
    language = data.get('language')
    
    print(f"Letter: '{letter}', Language: '{language}'")
    
    if not letter:
        print("ERROR: No letter provided")
        return jsonify({'error': 'No letter provided'}), 400
    
    # Map language names to gTTS language codes
    language_map = {
        'hindi': 'hi',
        'gujarati': 'gu', 
        'tamil': 'ta',
        'bengali': 'bn',
        'telugu': 'te',
        'marathi': 'mr',
        'punjabi': 'pa',
        'urdu': 'ur',
        'english': 'en'
    }
    
    # Get language code, default to Hindi if not found
    target_lang_lower = language.lower() if language else 'hindi'
    lang_code = language_map.get(target_lang_lower, 'hi')
    
    print(f"Playing letter: {letter} in {language} (code: {lang_code})")
    print(f"Using gTTS language code: {lang_code}")
    
    try:
        # Create a temporary file
        import tempfile
        import os
        
        print("Creating gTTS object...")
        # Create gTTS object with correct language
        tts = gTTS(text=letter, lang=lang_code, slow=True)
        print("gTTS object created successfully")
        
        # Create a temporary file
        print("Creating temporary file...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            # Save the audio to the temporary file
            print(f"Saving audio to temporary file: {temp_file.name}")
            tts.save(temp_file.name)
            temp_path = temp_file.name
        
        print(f"Audio file created at: {temp_path}")
        print(f"File size: {os.path.getsize(temp_path)} bytes")
        
        # Send the file
        @after_this_request
        def remove_file(response):
            try:
                print(f"Removing temporary file: {temp_path}")
                os.remove(temp_path)
                print("Temporary file removed successfully")
            except Exception as e:
                print(f"Error removing temporary file: {e}")
            return response
        
        print("Sending audio file to client...")
        return send_file(
            temp_path,
            mimetype='audio/mpeg',
            as_attachment=False
        )
        
    except Exception as e:
        print(f"ERROR generating audio: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/play_word', methods=['POST'])
def play_word():
    """Play audio for translated vocabulary words"""
    print("=== PLAY_WORD ROUTE CALLED ===")
    if 'user' not in session:
        print("ERROR: User not authenticated")
        return jsonify({'error': 'Not authenticated'}), 401
    
    print(f"User in session: {session.get('user')}")
    data = request.get_json()
    print(f"Received data: {data}")
    
    word = data.get('word') or data.get('text') or ''
    language = data.get('language') or data.get('target_language') or 'Hindi'
    
    print(f"Word: '{word}', Language: '{language}'")
    
    if not word.strip():
        print("ERROR: No word provided")
        return jsonify({'error': 'No word provided'}), 400
    
    # Map language names to gTTS language codes
    language_map = {
        'hindi': 'hi',
        'gujarati': 'gu', 
        'tamil': 'ta',
        'bengali': 'bn',
        'telugu': 'te',
        'marathi': 'mr',
        'punjabi': 'pa',
        'urdu': 'ur',
        'english': 'en'
    }
    
    # Get language code, default to Hindi if not found
    target_lang_lower = language.lower() if language else 'hindi'
    lang_code = language_map.get(target_lang_lower, 'hi')
    
    print(f"Playing word: {word} in {language} (code: {lang_code})")
    print(f"Using gTTS language code: {lang_code}")
    
    try:
        # Create a temporary file
        import tempfile
        import os
        
        print("Creating gTTS object...")
        # Create gTTS object with correct language
        tts = gTTS(text=word, lang=lang_code, slow=False)  # Words don't need slow speech
        print("gTTS object created successfully")
        
        # Create a temporary file
        print("Creating temporary file...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            # Save the audio to the temporary file
            print(f"Saving audio to temporary file: {temp_file.name}")
            tts.save(temp_file.name)
            temp_path = temp_file.name
        
        print(f"Audio file created at: {temp_path}")
        print(f"File size: {os.path.getsize(temp_path)} bytes")
        
        # Send the file
        @after_this_request
        def remove_file(response):
            try:
                print(f"Removing temporary file: {temp_path}")
                os.remove(temp_path)
                print("Temporary file removed successfully")
            except Exception as e:
                print(f"Error removing temporary file: {e}")
            return response
        
        print("Sending audio file to client...")
        return send_file(
            temp_path,
            mimetype='audio/mpeg',
            as_attachment=False
        )
        
    except Exception as e:
        print(f"ERROR generating audio: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        known_language = request.form.get('known_language')
        target_language = request.form.get('target_language')

        existing_user = User.find_by_username(username)
        if existing_user:
            return "Username already exists."

        new_user = User(
            username=username,
            known_language=known_language,
            target_language=target_language,
            level='beginner'
        )
        new_user.set_password(password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.find_by_username(username)

        if user and user.check_password(password):
            login_user(user)

            session['user'] = username  # Also set session for compatibility
            # If user was redirected to login from game route, send them back there
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            print("Login Successful")
            return redirect(url_for('language_selection'))
        return "Invalid credentials."
    return render_template('login.html')

@app.route('/language-selection', methods=['GET', 'POST'])
def language_selection():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        known = request.form['known_language']
        target = request.form['target_language']
        level = request.form['level']
        
        print(f"Language selection form data: known={known}, target={target}, level={level}")

        user = User.find_by_username(session['user'])
        if user:
            user.known_language = known
            user.target_language = target
            user.level = level
            user.save()
            
            print(f"User updated: {user.username}, target={user.target_language}, level={user.level}")

            # Redirect based on level, regardless of target language
            if level == 'beginner':
                print("Redirecting to beginner_choice")
                return redirect(url_for('beginner_choice'))
            elif level == 'intermediate':
                print("Redirecting to intermediate_levels")
                return redirect(url_for('intermediate_levels'))
            print("Redirecting to home (fallback)")
            return redirect(url_for('home'))

    return render_template('language_selection.html')

@app.route('/beginner-choice')
def beginner_choice():
    if 'user' not in session:
        print("No user in session, redirecting to login")
        return redirect(url_for('login'))
    user = User.find_by_username(session['user'])
    print(f"Beginner choice access: user={user.username if user else None}, target={user.target_language if user else None}, level={user.level if user else None}")
    if not user or not user.target_language or user.level != 'beginner':
        print("User doesn't meet beginner requirements, redirecting to home")
        return redirect(url_for('home'))
    return render_template('beginner_choice.html')

@app.route('/beginner-quiz')
def beginner_quiz():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.find_by_username(session['user'])
    if not user or not user.target_language or user.level != 'beginner':
        return redirect(url_for('home'))
    return redirect(url_for('game'))

@app.route('/beginner-pronunciation')
def beginner_pronunciation():
    """Beginner pronunciation practice page based on letters (vowels/consonants) for target language."""
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.find_by_username(session['user'])
    if not user or not user.target_language or user.level != 'beginner':
        return redirect(url_for('home'))

    # Default subset: vowels
    from native_content_system import get_language_letters
    letters = get_language_letters(user.target_language)

    # Build initial list (vowels by default)
    vocabulary_data = []
    for key, meta in letters.get('vowels', {}).items():
        vocabulary_data.append({
            'english': meta.get('letter', ''),            # reuse existing template variable to display the letter glyph
            'pronunciation': meta.get('pronunciation', ''),
            'transliteration': meta.get('transliteration', ''),
            'type': 'vowels'
        })

    return render_template(
        'beginner_pronunciation.html',
        vocabulary=vocabulary_data,
        target_language=user.target_language
    )

@app.route('/api/letters')
def api_letters():
    """Return letters for the given language and subset (vowels or consonants)."""
    language = request.args.get('language', 'hindi')
    subset = request.args.get('subset', 'vowels').lower()

    from native_content_system import get_language_letters
    letters = get_language_letters(language)

    if subset not in ('vowels', 'consonants'):
        subset = 'vowels'

    items = []
    for key, meta in letters.get(subset, {}).items():
        items.append({
            'key': key,
            'letter': meta.get('letter', ''),
            'pronunciation': meta.get('pronunciation', ''),
            'transliteration': meta.get('transliteration', ''),
            'type': subset
        })

    return jsonify({
        'success': True,
        'subset': subset,
        'language': language,
        'items': items
    })

@app.route('/generate-audio', methods=['GET'])
def generate_audio():
    text = request.args.get('text', '')
    if not text:
        return "No text provided", 400
    
    try:
        tts = gTTS(text=text, lang='hi')
        temp_file = "temp_audio.mp3"
        tts.save(temp_file)
        
        @after_this_request
        def remove_file(response):
            try:
                os.remove(temp_file)
            except Exception as error:
                app.logger.error(f"Error removing or closing downloaded file handle: {error}")
            return response
            
        return send_file(temp_file, mimetype="audio/mpeg")
    except Exception as e:
        return str(e), 500

@app.route('/intermediate')
def intermediate_levels():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.find_by_username(session['user'])
    if user is None:
        session.pop('user', None)
        return redirect(url_for('login'))
    if not user.target_language or user.level != 'intermediate':
        return redirect(url_for('home'))

    # Get progress for all levels
    progress_level1 = UserProgress.get_level_progress(user._id, 'intermediate_level_1')
    progress_level2 = UserProgress.get_level_progress(user._id, 'intermediate_level_2')
    progress_level3 = UserProgress.get_level_progress(user._id, 'intermediate_level_3')
    progress_level4 = UserProgress.get_level_progress(user._id, 'intermediate_level_4')
    progress_level5 = UserProgress.get_level_progress(user._id, 'intermediate_level_5')
    
    score1 = int(progress_level1.score) if progress_level1 and progress_level1.score is not None else 0
    score2 = int(progress_level2.score) if progress_level2 and progress_level2.score is not None else 0
    score3 = int(progress_level3.score) if progress_level3 and progress_level3.score is not None else 0
    score4 = int(progress_level4.score) if progress_level4 and progress_level4.score is not None else 0
    score5 = int(progress_level5.score) if progress_level5 and progress_level5.score is not None else 0
    
    passed_level1 = score1 >= 60
    passed_level2 = score2 >= 60
    passed_level3 = score3 >= 60
    passed_level4 = score4 >= 60
    passed_level5 = score5 >= 60

    return render_template('intermediate_levels.html', 
                         score1=score1, score2=score2, score3=score3, score4=score4, score5=score5,
                         passed_level1=passed_level1, passed_level2=passed_level2, passed_level3=passed_level3, passed_level4=passed_level4, passed_level5=passed_level5)

@app.route('/intermediate/<int:level>')
def intermediate_level(level):
    print('Session user:', session.get('user'))
    if 'user' not in session:
        print('Not logged in')
        return redirect(url_for('login'))
    user = User.find_by_username(session['user'])
    print('User:', user)
    if user is None:
        print('User not found in DB')
        session.pop('user', None)
        return redirect(url_for('login'))
    print('Target language:', user.target_language, 'Level:', user.level)
    if not user.target_language or user.level != 'intermediate':
        print('User does not meet target language/intermediate requirement')
        return render_template('intermediate_levels.html', error='You must select a target language and intermediate level to access this content.')

    # Check level prerequisites
    progress_level1 = UserProgress.get_level_progress(user._id, 'intermediate_level_1')
    progress_level2 = UserProgress.get_level_progress(user._id, 'intermediate_level_2')
    progress_level3 = UserProgress.get_level_progress(user._id, 'intermediate_level_3')
    score1 = int(progress_level1.score) if progress_level1 and progress_level1.score is not None else 0
    score2 = int(progress_level2.score) if progress_level2 and progress_level2.score is not None else 0
    score3 = int(progress_level3.score) if progress_level3 and progress_level3.score is not None else 0
    # Level 2 requires Level 1 completion
    if level == 2 and score1 < 60:
        return redirect(url_for('intermediate_levels'))
    # Level 3 requires Level 2 completion
    if level == 3 and score2 < 60:
        return redirect(url_for('intermediate_levels'))
    # Level 4 requires Level 3 completion
    if level == 4 and score3 < 60:
        return redirect(url_for('intermediate_levels'))
    # Route to specific level pages with vocabulary
    # Image extension mapping for exact file paths
    image_extensions = {
        # Fruits
        'apple': 'jpeg',
        'banana': 'jpg', 
        'cherry': 'jpeg',
        'grapes': 'jpeg',
        'kiwi': 'jpeg',
        'lichi': 'jpeg',
        'mango': 'jpg',
        'orange': 'jpeg',
        'papaya': 'jpeg',
        'pear': 'jpeg',
        'pineapple': 'jpeg',
        'pomegranate': 'jpeg',
        'strawberry': 'jpeg',
        'sugarcane': 'jpeg',
        'watermelon': 'jpeg',
        # Animals  
        'cow': 'jpg',
        'dog': 'jpg',
        'cat': 'jpeg',
        'horse': 'jpeg',
        'elephant': 'JPG',
        'tiger': 'jpg',
        'lion': 'jpeg',
        'monkey': 'jpeg',
        'bear': 'jpeg',
        'fox': 'jpeg',
        'rabbit': 'jpeg',
        'deer': 'jpeg',
        'goat': 'jpeg',
        'sheep': 'jpeg',
        'pig': 'jpeg',
        'duck': 'jpeg',
        'chicken': 'jpeg',
        'peacock': 'jpeg',
        'parrot': 'jpeg',
        'eagle': 'jpeg',
        'snake': 'jpeg',
        'frog': 'jpeg',
        'fish': 'jpeg',
        'butterfly': 'jpeg',
        'ant': 'jpeg',
        'bee': 'jpeg',
        # Vegetables
        'tomato': 'jpeg',
        'onion': 'jpeg', 
        'potato': 'jpg',
        'carrot': 'jpeg',
        'cabbage': 'jpg',
        'cauliflower': 'jpeg',
        'brinjal': 'jpg',
        'chilli': 'jpg',
        'pumpkin': 'jpeg',
        'spinach': 'jpg',
        'peas': 'jpeg',
        'mushroom': 'jpeg',
        'lady_finger': 'jpg',
        'bottle_gourd': 'jpeg',
        'bitter_gourd': 'jpg',
        'capcicum': 'jpeg'
    }
    
    level_category_mapping = {
        1: 'fruits',  # Level 1 shows fruits
        2: 'animals', 
        3: 'colors',
        4: 'professionals',  # Level 4 shows professionals
        5: 'body_parts'
    }
    
    category = level_category_mapping.get(level, 'fruits')
    
    # Get English vocabulary
    english_words = get_english_vocabulary(category)
    
    # Translate to target language using IndicTrans2
    translated_vocab = translation_service.translate_vocabulary_category(
        category, user.target_language
    )
    
    # Format vocabulary for template (translated_vocab is already a list of dicts)
    vocabulary_items = []
    for vocab_item in translated_vocab:
        english_word = vocab_item.get('english', '')
        vocabulary_items.append({
            'english': english_word,
            'translation': vocab_item.get('translated', vocab_item.get('english', '')),
            'category': category,
            'image_ext': image_extensions.get(english_word.lower(), 'jpg')  # Default to jpg if not found
        })
    
    print(f"Passing {len(vocabulary_items)} vocabulary items to template")
    for i, item in enumerate(vocabulary_items[:3]):  # Show first 3
        print(f"  {i+1}. {item['english']} -> {item['translation']}")
    
    if level == 2:
        print('Rendering intermediate_level2.html')
        return render_template('intermediate_level2.html', 
                             vocabulary=vocabulary_items, 
                             category=category,
                             target_language=user.target_language)
    elif level == 3:
        print('Rendering intermediate_level3.html')
        return render_template('intermediate_level3.html',
                             vocabulary=vocabulary_items, 
                             category=category,
                             target_language=user.target_language)
    elif level == 4:
        print('Rendering intermediate_level4.html')
        return render_template('intermediate_level4.html',
                             vocabulary=vocabulary_items, 
                             category=category,
                             target_language=user.target_language)
    elif level == 5:
        print('Rendering intermediate_level5.html')
        return render_template('intermediate_level5.html',
                             vocabulary=vocabulary_items, 
                             category=category,
                             target_language=user.target_language)
    
    print(f'Rendering intermediate_level{level}.html')
    return render_template(f'intermediate_level{level}.html',
                         vocabulary=vocabulary_items, 
                         category=category,
                         target_language=user.target_language)

@app.route('/intermediate/<int:level>/quiz')
def intermediate_level_quiz(level):
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.find_by_username(session['user'])
    if user is None:
        session.pop('user', None)
        return redirect(url_for('login'))
    
    # Route to specific quiz pages
    if level == 2:
        return render_template('intermediate_level2_quiz.html')
    elif level == 3:
        return render_template('intermediate_level3_quiz.html')
    
    return render_template(f'intermediate_level{level}_quiz.html')

@app.route('/update-level-score', methods=['POST'])
def update_level_score():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    level = data.get('level')
    score = data.get('score')
    
    if not level or score is None:
        return jsonify({'error': 'Missing level or score'}), 400
    
    user = User.find_by_username(session['user'])
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    # Save user progress to MongoDB
    progress = UserProgress(
        user_id=str(user._id),
        level=f'intermediate_level_{level}',
        score=score,
        completed=(score >= 80)  # Pass mark is 80%
    )
    progress.save()
    
    if score >= 80:
        return jsonify({'success': True, 'nextLevelUnlocked': True})
    
    return jsonify({'success': True, 'nextLevelUnlocked': False})

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

# ============================================================================
# ENHANCED LEVEL ROUTES WITH TRANSLATION SUPPORT
# ============================================================================

from comprehensive_vocabulary import get_vocabulary_for_level, translate_level_content
from datetime import datetime

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
        
        # Use indictrans2 service for translation
        content = LEVEL_CONTENT.get(level, {})
        translated_content = {}
        
        # Translate each text field in the content
        for key, value in content.items():
            if isinstance(value, str):
                translated_content[key] = translation_service.translate_text(value, language)
            else:
                translated_content[key] = value
        
        return jsonify(translated_content)
    
    except Exception as e:
        print(f"Error translating content: {e}")
        return jsonify({'error': 'Translation failed'}), 500

@app.route('/api/level-vocabulary/<level>')
def get_level_vocabulary_api(level):
    """API endpoint to get vocabulary for a specific level"""
    try:
        language = request.args.get('language', 'english')
        vocabulary = get_vocabulary_for_level(level, language)
        return jsonify(vocabulary)
    
    except Exception as e:
        print(f"Error getting vocabulary: {e}")
        return jsonify({'error': 'Failed to get vocabulary'}), 500

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
        questions = generate_enhanced_quiz_questions(vocabulary, int(level))
        
        # Translate questions using indictrans2 service
        translated_questions = []
        for question in questions:
            translated_question = {
                'question': translation_service.translate_text(question.get('question', ''), language),
                'options': [translation_service.translate_text(option, language) for option in question.get('options', [])],
                'correct': question.get('correct', 0),
                'explanation': translation_service.translate_text(question.get('explanation', ''), language)
            }
            translated_questions.append(translated_question)
        
        return jsonify({
            'success': True,
            'questions': translated_questions
        })
    
    except Exception as e:
        print(f"Error translating quiz: {e}")
        return jsonify({'error': 'Translation failed'}), 500

def generate_enhanced_quiz_questions(vocabulary, level, num_questions=5):
    """Generate enhanced quiz questions from vocabulary"""
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
        print(f"Error generating quiz questions: {e}")
        return []

@app.route('/api/submit-enhanced-quiz', methods=['POST'])
def submit_enhanced_quiz():
    """Enhanced quiz submission with progress tracking"""
    try:
        if 'user' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        data = request.get_json()
        level = data.get('level')
        answers = data.get('answers', {})
        
        # Calculate score
        total_questions = len(answers)
        correct_answers = sum(1 for answer in answers.values() if answer.get('correct', False))
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Update user progress
        user = User.find_by_username(session['user'])
        if user:
            progress = UserProgress(
                user_id=str(user._id),
                level=f'intermediate_level_{level}',
                score=score,
                completed=(score >= 60)  # 60% to pass
            )
            progress.save()
        
        return jsonify({
            'success': True,
            'score': score,
            'correct': correct_answers,
            'total': total_questions,
            'passed': score >= 60
        })
    
    except Exception as e:
        print(f"Error submitting quiz: {e}")
        return jsonify({'error': 'Failed to submit quiz'}), 500

# Language support API
@app.route('/api/supported-languages')
def get_supported_languages():
    """Get list of supported languages"""
    try:
        # Use indictrans2 service supported languages
        languages = list(translation_service.supported_languages)
        
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
        print(f"Error getting supported languages: {e}")
        return jsonify({'error': 'Failed to get languages'}), 500

# User language preference
@app.route('/api/user-language', methods=['GET', 'POST'])
def user_language_preference():
    """Get or set user language preference"""
    try:
        if 'user' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        user = User.find_by_username(session['user'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if request.method == 'POST':
            # Set language preference
            data = request.get_json()
            language = data.get('language', 'english')
            
            # Store in user document or separate preferences collection
            db = mongo.db
            preferences_collection = db.user_language_preferences
            
            preferences_collection.update_one(
                {'user_id': str(user._id)},
                {'$set': {'preferred_language': language, 'updated_at': datetime.utcnow()}},
                upsert=True
            )
            
            return jsonify({'success': True, 'language': language})
        
        else:
            # Get language preference
            db = mongo.db
            preferences_collection = db.user_language_preferences
            preference = preferences_collection.find_one({'user_id': str(user._id)})
            language = preference.get('preferred_language', 'english') if preference else 'english'
            return jsonify({'language': language})
    
    except Exception as e:
        print(f"Error handling user language preference: {e}")
        return jsonify({'error': 'Failed to handle language preference'}), 500
