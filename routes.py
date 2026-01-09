from flask import render_template, request, redirect, url_for, session, jsonify, send_file, after_this_request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from mongodb_models import User, UserProgress, mongo
from app import app, login_manager
from native_content_system import get_language_letters, get_english_vocabulary, get_all_vocabulary_categories
from translation_service import translation_service
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
            elif level == 'advanced':
                print("Redirecting to advanced_levels")
                return redirect(url_for('advanced_levels'))
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
        print('Rendering enhanced intermediate template with pronunciation for level 2')
        return render_template('enhanced_intermediate_pronunciation.html', 
                             level=level,
                             level_title='Animals and Birds',
                             target_language=user.target_language,
                             speech_lang=get_speech_recognition_lang(user.target_language))
    elif level == 3:
        print('Rendering enhanced intermediate template with pronunciation for level 3')
        return render_template('enhanced_intermediate_pronunciation.html',
                             level=level,
                             level_title='Colors',
                             target_language=user.target_language,
                             speech_lang=get_speech_recognition_lang(user.target_language))
    elif level == 4:
        print('Rendering enhanced intermediate template with pronunciation for level 4')
        return render_template('enhanced_intermediate_pronunciation.html',
                             level=level,
                             level_title='Body Parts',
                             target_language=user.target_language,
                             speech_lang=get_speech_recognition_lang(user.target_language))
    elif level == 5:
        print('Rendering enhanced intermediate template with pronunciation for level 5')
        return render_template('enhanced_intermediate_pronunciation.html',
                             level=level,
                             level_title='Family Relations',
                             target_language=user.target_language,
                             speech_lang=get_speech_recognition_lang(user.target_language))
    
    # Default case for level 1 and others
    level_titles = {
        1: 'Fruits and Vegetables',
        2: 'Animals and Birds',
        3: 'Colors',
        4: 'Body Parts', 
        5: 'Family Relations'
    }
    
    print(f'Rendering enhanced intermediate template with pronunciation for level {level}')
    return render_template('enhanced_intermediate_pronunciation.html',
                         level=level,
                         level_title=level_titles.get(level, f'Level {level}'),
                         target_language=user.target_language,
                         speech_lang=get_speech_recognition_lang(user.target_language))

@app.route('/intermediate/<int:level>/quiz')
def intermediate_level_quiz(level):
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.find_by_username(session['user'])
    if user is None:
        session.pop('user', None)
        return redirect(url_for('login'))
    
    # Route to all available quiz pages
    if level == 1:
        return render_template('intermediate_level1_quiz.html', target_language=user.target_language)
    elif level == 2:
        return render_template('intermediate_level2_quiz.html', target_language=user.target_language)
    elif level == 3:
        return render_template('intermediate_level3_quiz.html', target_language=user.target_language)
    elif level == 4:
        return render_template('intermediate_level4_quiz.html', target_language=user.target_language)
    elif level == 5:
        return render_template('intermediate_level5_quiz.html', target_language=user.target_language)
    
    # Default fallback
    return render_template(f'intermediate_level{level}_quiz.html', target_language=user.target_language)

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


def get_speech_recognition_lang(target_language):
    """Map target language to appropriate speech recognition language code"""
    language_mapping = {
        'hindi': 'hi-IN',
        'gujarati': 'gu-IN', 
        'marathi': 'mr-IN',
        'bengali': 'bn-IN',
        'tamil': 'ta-IN',
        'telugu': 'te-IN',
        'kannada': 'kn-IN',
        'malayalam': 'ml-IN',
        'punjabi': 'pa-IN',
        'urdu': 'ur-PK',
        'assamese': 'as-IN',
        'odia': 'hi-IN',  # Fallback to Hindi as Odia might not be supported
        'sanskrit': 'hi-IN',  # Fallback to Hindi
    }
    return language_mapping.get(target_language.lower(), 'hi-IN')

@app.route('/api/get-pronunciation-data', methods=['POST'])
def get_pronunciation_data():
    """Get pronunciation data for a word in target language"""
    try:
        if 'user' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        user = User.find_by_username(session['user'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        english_word = data.get('word', '')
        target_language = data.get('language') or user.target_language
        
        if not english_word or not target_language:
            return jsonify({'error': 'Missing word or language'}), 400
        
        # Get translation from IndicTrans2 (keeping existing translation system unchanged)
        translated_word = translation_service.translate_text(english_word, target_language)
        
        # Get pronunciation from comprehensive vocabulary if available
        from comprehensive_vocabulary import COMPREHENSIVE_VOCABULARY
        pronunciation = ""
        
        # Search for the word in comprehensive vocabulary
        for category, words in COMPREHENSIVE_VOCABULARY.items():
            for key, word_data in words.items():
                if word_data['english'].lower() == english_word.lower():
                    pronunciation = word_data.get('pronunciation', '')
                    break
            if pronunciation:
                break
        
        # If no specific pronunciation found, use the translated word as pronunciation guide
        if not pronunciation:
            pronunciation = translated_word
        
        # Generate pronunciation variants for better matching
        variants = [
            pronunciation.lower(),
            translated_word.lower(),
            english_word.lower()
        ]
        
        # Add common pronunciation variations
        if pronunciation:
            # Remove special characters and create phonetic variants
            clean_pronunciation = ''.join(c for c in pronunciation.lower() if c.isalpha())
            if clean_pronunciation and clean_pronunciation != pronunciation.lower():
                variants.append(clean_pronunciation)
        
        return jsonify({
            'english': english_word,
            'translation': translated_word,
            'pronunciation': pronunciation,
            'variants': list(set(variants)),  # Remove duplicates
            'language': target_language
        })
        
    except Exception as e:
        print(f"Error getting pronunciation data: {e}")
        return jsonify({'error': 'Failed to get pronunciation data'}), 500

@app.route('/api/evaluate-pronunciation', methods=['POST'])
def evaluate_pronunciation():
    """Evaluate pronunciation accuracy using fuzzy matching"""
    try:
        if 'user' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        if not data:
            print("Error: No JSON data received")
            return jsonify({'error': 'No data received'}), 400
        
        print(f"Received pronunciation evaluation request: {data}")
        
        spoken_text = data.get('spoken_text', '').lower().strip()
        expected_variants = data.get('expected_variants', [])
        
        print(f"Spoken text: '{spoken_text}'")
        print(f"Expected variants: {expected_variants}")
        
        if not spoken_text:
            print("Error: Missing spoken text")
            return jsonify({'error': 'Missing spoken text'}), 400
            
        if not expected_variants:
            print("Error: Missing expected variants")
            return jsonify({'error': 'Missing expected variants'}), 400
        
        # Calculate similarity scores against all variants
        best_score = 0
        best_match = ""
        
        for variant in expected_variants:
            if not variant:
                continue
                
            variant_lower = variant.lower().strip()
            
            # Exact match gets perfect score
            if spoken_text == variant_lower:
                best_score = 100
                best_match = variant
                break
            
            # Calculate Levenshtein distance
            distance = levenshtein_distance(spoken_text, variant_lower)
            max_len = max(len(spoken_text), len(variant_lower))
            
            if max_len == 0:
                similarity = 100
            else:
                similarity = max(0, (1 - distance / max_len) * 100)
            
            if similarity > best_score:
                best_score = similarity
                best_match = variant
        
        # Determine feedback based on score
        if best_score >= 85:
            feedback = "Excellent pronunciation!"
            status = "correct"
        elif best_score >= 70:
            feedback = "Good pronunciation, minor improvements needed."
            status = "partial"
        elif best_score >= 50:
            feedback = "Fair pronunciation, keep practicing."
            status = "partial"
        else:
            feedback = "Keep practicing! Try to match the pronunciation more closely."
            status = "incorrect"
        
        return jsonify({
            'score': round(best_score, 1),
            'feedback': feedback,
            'status': status,
            'best_match': best_match,
            'spoken': spoken_text
        })
        
    except Exception as e:
        print(f"Error evaluating pronunciation: {e}")
        return jsonify({'error': 'Failed to evaluate pronunciation'}), 500

def levenshtein_distance(s1, s2):
    """Calculate Levenshtein distance between two strings"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    
    return prev_row[-1]

@app.route('/api/vocabulary/<int:level>')
def get_level_vocabulary(level):
    """Get vocabulary for a specific intermediate level with pronunciation data"""
    try:
        if 'user' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        user = User.find_by_username(session['user'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Level to category mapping
        level_categories = {
            1: ['fruits', 'vegetables'],
            2: ['animals', 'birds'],
            3: ['colors'],
            4: ['body_parts'],
            5: ['family_relations']
        }
        
        categories = level_categories.get(level, [])
        vocabulary_data = []
        
        from comprehensive_vocabulary import COMPREHENSIVE_VOCABULARY
        
        # Image extension mapping
        image_extensions = {
            # Fruits
            'apple': 'jpeg', 'banana': 'jpg', 'cherry': 'jpeg', 'grapes': 'jpeg',
            'kiwi': 'jpeg', 'lychee': 'jpeg', 'mango': 'jpg', 'orange': 'jpeg',
            'papaya': 'jpeg', 'pear': 'jpeg', 'pineapple': 'jpeg', 'pomegranate': 'jpeg',
            'strawberry': 'jpeg', 'watermelon': 'jpeg',
            # Animals  
            'cow': 'jpg', 'dog': 'jpg', 'cat': 'jpeg', 'horse': 'jpeg', 'elephant': 'JPG',
            'lion': 'jpeg', 'tiger': 'jpeg', 'monkey': 'jpeg', 'bear': 'jpeg',
            'rabbit': 'jpg', 'deer': 'jpeg', 'goat': 'jpeg', 'sheep': 'jpeg',
            'duck': 'jpeg', 'chicken': 'jpeg', 'peacock': 'jpeg', 'parrot': 'jpeg',
            'snake': 'jpeg', 'frog': 'jpeg', 'fish': 'jpeg', 'butterfly': 'jpeg'
        }
        
        for category in categories:
            if category in COMPREHENSIVE_VOCABULARY:
                for key, word_data in COMPREHENSIVE_VOCABULARY[category].items():
                    english_word = word_data['english']
                    pronunciation = word_data.get('pronunciation', '')
                    
                    # Get translation using existing translation service (unchanged)
                    try:
                        translation = translation_service.translate_text(english_word, user.target_language)
                    except:
                        translation = pronunciation if pronunciation else english_word
                    
                    vocabulary_data.append({
                        'english': english_word,
                        'translation': translation,
                        'pronunciation': pronunciation,
                        'category': category,
                        'image_path': f'/static/images/{category}/{english_word.lower()}.{image_extensions.get(english_word.lower(), "jpg")}'
                    })
        
        return jsonify({'vocabulary': vocabulary_data})
        
    except Exception as e:
        print(f"Error getting vocabulary: {e}")
        return jsonify({'error': 'Failed to get vocabulary'}), 500
# ==================== ADVANCED LEVEL ROUTES ====================

@app.route('/advanced_levels')
def advanced_levels():
    """Advanced level selection page showing all sentence categories"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = User.find_by_username(session['user'])
    if not user:
        session.pop('user', None)
        return redirect(url_for('login'))
    
    if not user.target_language or user.level != 'advanced':
        return render_template('advanced_levels.html', 
                             error='You must select a target language and advanced level to access this content.')
    
    # Get progress for each category
    from native_content_system import get_all_sentence_categories
    categories = get_all_sentence_categories()
    
    progress_data = {}
    for category in categories:
        progress = UserProgress.get_level_progress(user._id, f'advanced_{category}')
        progress_data[category] = {
            'score': int(progress.score) if progress and progress.score is not None else 0,
            'completed': progress and progress.completed
        }
    
    return render_template('advanced_levels.html',
                         target_language=user.target_language,
                         known_language=user.known_language,
                         categories=categories,
                         progress=progress_data)

@app.route('/advanced/<category>')
def advanced_level(category):
    """Advanced level learning page for specific sentence category"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = User.find_by_username(session['user'])
    if not user:
        session.pop('user', None)
        return redirect(url_for('login'))
    
    if not user.target_language or user.level != 'advanced':
        return redirect(url_for('advanced_levels'))
    
    from native_content_system import get_advanced_sentences, get_all_sentence_categories
    
    # Validate category
    valid_categories = get_all_sentence_categories()
    if category not in valid_categories:
        return redirect(url_for('advanced_levels'))
    
    # Get English sentences
    english_sentences = get_advanced_sentences(category)
    
    # Translate sentences to target language
    translated_sentences = []
    for sentence_data in english_sentences:
        english_text = sentence_data['english']
        try:
            translation = translation_service.translate_text(english_text, user.target_language)
        except Exception as e:
            print(f"Translation error: {e}")
            translation = english_text
        
        translated_sentences.append({
            'english': english_text,
            'translation': translation,
            'context': sentence_data.get('context', '')
        })
    
    category_titles = {
        'greetings': 'Greetings and Pleasantries',
        'introductions': 'Introducing Yourself',
        'daily_activities': 'Daily Activities',
        'questions': 'Common Questions',
        'shopping': 'Shopping Conversations',
        'directions': 'Asking for Directions'
    }
    
    return render_template('advanced_level.html',
                         category=category,
                         category_title=category_titles.get(category, category.title()),
                         sentences=translated_sentences,
                         target_language=user.target_language,
                         speech_lang=get_speech_recognition_lang(user.target_language))

@app.route('/advanced/<category>/quiz')
def advanced_level_quiz(category):
    """Quiz page for advanced level sentence category"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = User.find_by_username(session['user'])
    if not user:
        session.pop('user', None)
        return redirect(url_for('login'))
    
    if not user.target_language or user.level != 'advanced':
        return redirect(url_for('advanced_levels'))
    
    from native_content_system import get_advanced_sentences, get_all_sentence_categories
    
    # Validate category
    valid_categories = get_all_sentence_categories()
    if category not in valid_categories:
        return redirect(url_for('advanced_levels'))
    
    # Get and translate sentences for quiz
    english_sentences = get_advanced_sentences(category)
    translated_sentences = []
    
    for sentence_data in english_sentences:
        english_text = sentence_data['english']
        try:
            translation = translation_service.translate_text(english_text, user.target_language)
        except Exception as e:
            print(f"Translation error: {e}")
            translation = english_text
        
        translated_sentences.append({
            'english': english_text,
            'translation': translation
        })
    
    category_titles = {
        'greetings': 'Greetings and Pleasantries',
        'introductions': 'Introducing Yourself',
        'daily_activities': 'Daily Activities',
        'questions': 'Common Questions',
        'shopping': 'Shopping Conversations',
        'directions': 'Asking for Directions'
    }
    
    return render_template('advanced_level_quiz.html',
                         category=category,
                         category_title=category_titles.get(category, category.title()),
                         sentences=translated_sentences,
                         target_language=user.target_language)

@app.route('/advanced/<category>/submit', methods=['POST'])
def advanced_level_submit(category):
    """Submit advanced level quiz results"""
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.find_by_username(session['user'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        data = request.get_json()
        score = data.get('score', 0)
        total = data.get('total', 0)
        
        # Calculate percentage
        percentage = int((score / total * 100) if total > 0 else 0)
        
        # Save progress
        level_name = f'advanced_{category}'
        UserProgress.update_or_create(
            user_id=user._id,
            level=level_name,
            score=percentage,
            completed=(percentage >= 60)
        )
        
        return jsonify({
            'success': True,
            'score': score,
            'total': total,
            'percentage': percentage,
            'passed': percentage >= 60
        })
        
    except Exception as e:
        print(f"Error submitting quiz: {e}")
        return jsonify({'error': 'Failed to submit quiz'}), 500

@app.route('/api/advanced/evaluate_pronunciation', methods=['POST'])
def evaluate_advanced_pronunciation():
    """Evaluate pronunciation for advanced level sentences"""
    try:
        if 'user' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        user = User.find_by_username(session['user'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        recognized_text = data.get('recognized_text', '').strip().lower()
        expected_text = data.get('expected_text', '').strip().lower()
        
        if not recognized_text or not expected_text:
            return jsonify({'error': 'Missing text data'}), 400
        
        # Calculate similarity using Levenshtein distance
        distance = levenshtein_distance(recognized_text, expected_text)
        max_len = max(len(recognized_text), len(expected_text))
        
        if max_len == 0:
            similarity = 100
        else:
            similarity = int(((max_len - distance) / max_len) * 100)
        
        # Determine if pronunciation is acceptable
        is_correct = similarity >= 70  # 70% similarity threshold
        
        feedback = {
            'similarity': similarity,
            'is_correct': is_correct,
            'recognized': recognized_text,
            'expected': expected_text
        }
        
        if similarity >= 90:
            feedback['message'] = 'Excellent pronunciation!'
        elif similarity >= 70:
            feedback['message'] = 'Good pronunciation!'
        elif similarity >= 50:
            feedback['message'] = 'Fair. Keep practicing!'
        else:
            feedback['message'] = 'Try again. Listen carefully and repeat.'
        
        return jsonify(feedback)
        
    except Exception as e:
        print(f"Error evaluating pronunciation: {e}")
        return jsonify({'error': 'Failed to evaluate pronunciation'}), 500