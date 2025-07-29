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
            # If user was redirected to login from game route, send them back there
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
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

        # Redirect to game page instead of home
        return redirect(url_for('game'))

    return render_template('language_selection.html')

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
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
