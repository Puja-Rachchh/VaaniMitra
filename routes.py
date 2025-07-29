from flask import render_template, request, redirect, url_for, session, jsonify, send_file, after_this_request
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from app import app, db
import os
import random
from gtts import gTTS

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
            session['user'] = user.username
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

        if target == 'Hindi' and level == 'Beginner':
            return redirect(url_for('beginner_choice'))
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

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
