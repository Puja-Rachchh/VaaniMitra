from flask import render_template, request, redirect, url_for, session, jsonify, send_file, after_this_request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from app import app, db, login_manager
import os
import random
from gtts import gTTS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/home')
def home():
    if 'user' in session:
        user = User.query.filter_by(username=session['user']).first()
        return render_template('index.html', username=user.username, known=user.known_language, target=user.target_language, level=user.level)
    return redirect(url_for('login'))

    if 'user' not in session:
        print('Not logged in')
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    print('User:', user)
    if user is None:
        print('User not found in DB')
        session.pop('user', None)
        return redirect(url_for('login'))
    print('Target language:', user.target_language, 'Level:', user.level)
    if user.target_language != 'Hindi' or user.level != 'Intermediate':
        print('User does not meet Hindi/Intermediate requirement')
        return render_template('intermediate_levels.html', error='You must select Hindi and Intermediate level to access this content.')
@app.route('/hindi_letters')
def hindi_letters():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    if user.target_language != 'Hindi' or user.level != 'Beginner':
        return redirect(url_for('home'))
    return render_template('hindi_letters.html')

@app.route('/play_hindi_letter', methods=['POST'])
def play_hindi_letter():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    letter = data.get('letter')
    
    if not letter:
        return jsonify({'error': 'No letter provided'}), 400
    
    try:
        # Create a temporary file
        import tempfile
        import os
        
        # Create gTTS object with Hindi language
        tts = gTTS(text=letter, lang='hi')
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            # Save the audio to the temporary file
            tts.save(temp_file.name)
            temp_path = temp_file.name
        
        # Send the file
        @after_this_request
        def remove_file(response):
            try:
                os.remove(temp_path)
            except Exception as e:
                print(f"Error removing temporary file: {e}")
            return response
        
        return send_file(
            temp_path,
            mimetype='audio/mpeg',
            as_attachment=False
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists."

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password=hashed_password,
            known_language=None,
            target_language=None,
            level=None
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
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

        user = User.query.filter_by(username=session['user']).first()
        user.known_language = known
        user.target_language = target
        user.level = level
        db.session.commit()

        if target == 'Hindi':
            if level == 'Beginner':
                return redirect(url_for('beginner_choice'))
            elif level == 'Intermediate':
                return redirect(url_for('intermediate_levels'))
        return redirect(url_for('home'))

    return render_template('language_selection.html')

@app.route('/beginner-choice')
def beginner_choice():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    if user.target_language != 'Hindi' or user.level != 'Beginner':
        return redirect(url_for('home'))
    return render_template('beginner_choice.html')

@app.route('/beginner-quiz')
def beginner_quiz():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    if user.target_language != 'Hindi' or user.level != 'Beginner':
        return redirect(url_for('home'))
    return redirect(url_for('game'))

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
                app.logger.error("Error removing or closing downloaded file handle", error)
            return response
            
        return send_file(temp_file, mimetype="audio/mpeg")
    except Exception as e:
        return str(e), 500

@app.route('/intermediate')
def intermediate_levels():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    if user is None:
        session.pop('user', None)
        return redirect(url_for('login'))
    if user.target_language != 'Hindi' or user.level != 'Intermediate':
        return redirect(url_for('home'))
    return render_template('intermediate_levels.html')

@app.route('/intermediate/<int:level>')
def intermediate_level(level):
    print('Session user:', session.get('user'))
    if 'user' not in session:
        print('Not logged in')
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    print('User:', user)
    if user is None:
        print('User not found in DB')
        session.pop('user', None)
        return redirect(url_for('login'))
    print('Target language:', user.target_language, 'Level:', user.level)
    if user.target_language != 'Hindi' or user.level != 'Intermediate':
        print('User does not meet Hindi/Intermediate requirement')
        return render_template('intermediate_levels.html', error='You must select Hindi and Intermediate level to access this content.')
    # Level access is now open for all intermediate levels
    # Route Level 2 to animals page
    if level == 2:
        print('Rendering intermediate_level2.html')
        return render_template('intermediate_level2.html')
    print(f'Rendering intermediate_level{level}.html')
    return render_template(f'intermediate_level{level}.html')

@app.route('/intermediate/<int:level>/quiz')
def intermediate_level_quiz(level):
    if 'user' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    if user is None:
        session.pop('user', None)
        return redirect(url_for('login'))
    if user.target_language != 'Hindi' or user.level != 'Intermediate':
        return redirect(url_for('home'))
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
    
    user = User.query.filter_by(username=session['user']).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    # Update user's progress in the database
    setattr(user, f'intermediate_level_{level}_score', score)
    if score >= 80:  # Pass mark is 80%
        setattr(user, f'intermediate_level_{level}_completed', True)
        db.session.commit()
        return jsonify({'success': True, 'nextLevelUnlocked': True})
    
    db.session.commit()
    return jsonify({'success': True, 'nextLevelUnlocked': False})

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))
