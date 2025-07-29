from flask import render_template, request, jsonify, send_file, session, redirect, url_for
from app import app
import os
import random
from flask_login import login_required, current_user

@app.route('/game')
@login_required
def game():
    # login_required will automatically redirect to login if user is not authenticated
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    # Hindi characters and their pronunciations
    characters = {
        "अ": ["a", "aa", "i"],
        "आ": ["aa", "a", "e"],
        "इ": ["i", "ee", "u"],
        "ई": ["ee", "i", "ai"],
        "उ": ["u", "oo", "e"],
        "ऊ": ["oo", "u", "au"],
        "ऋ": ["ri", "ru", "ra"],
        "ए": ["e", "ai", "a"],
        "ऐ": ["ai", "e", "a"],
        "ओ": ["o", "au", "oo"],
        "औ": ["au", "o", "a"],
        "अं": ["an", "am", "a"],
        "अः": ["aha", "a", "ah"],
        "क": ["ka", "pa", "ta"],
        "ख": ["kha", "ka", "ga"],
        "ग": ["ga", "ka", "gha"],
        "घ": ["gha", "ga", "kha"],
        "ङ": ["nga", "na", "gna"],
        "च": ["cha", "chha", "ja"],
        "छ": ["chha", "cha", "kha"],
        "ज": ["ja", "cha", "zha"],
        "झ": ["jha", "ja", "dha"],
        "ञ": ["nya", "na", "nyaa"]
    }

    # Initialize or reset game session
    if 'game_data' not in session or 'current_question' not in session['game_data']:
        # Get 5 random characters for the quiz
        all_characters = list(characters.keys())
        quiz_characters = random.sample(all_characters, 5)
        session['game_data'] = {
            'lives': 3,  # Starting lives
            'score': 0,  # Current score
            'questions': quiz_characters,  # Store the 5 questions
            'current_question': 0,  # Track current question number
            'total_questions': 5,  # Total number of questions
            'incorrect_answers': []  # Track which questions were answered incorrectly
        }
    
    # If all questions are answered, show the final results
    if 'game_data' in session and session['game_data']['current_question'] >= session['game_data']['total_questions']:
        return redirect(url_for('game_results'))
    
    # Hindi characters and their pronunciations
    characters = {
        "अ": ["a", "aa", "i"],
        "आ": ["aa", "a", "e"],
        "इ": ["i", "ee", "u"],
        "ई": ["ee", "i", "ai"],
        "उ": ["u", "oo", "e"],
        "ऊ": ["oo", "u", "au"],
        "ऋ": ["ri", "ru", "ra"],
        "ए": ["e", "ai", "a"],
        "ऐ": ["ai", "e", "a"],
        "ओ": ["o", "au", "oo"],
        "औ": ["au", "o", "a"],
        "अं": ["an", "am", "a"],
        "अः": ["aha", "a", "ah"],

        # व्यंजन (Vyanjan) - Consonants
        "क": ["ka", "pa", "ta"],
        "ख": ["kha", "ka", "ga"],
        "ग": ["ga", "ka", "gha"],
        "घ": ["gha", "ga", "kha"],
        "ङ": ["nga", "na", "gna"],

        "च": ["cha", "chha", "ja"],
        "छ": ["chha", "cha", "kha"],
        "ज": ["ja", "cha", "zha"],
        "झ": ["jha", "ja", "dha"],
        "ञ": ["nya", "na", "nyaa"],

        "ट": ["ta", "tha", "da"],
        "ठ": ["tha", "ta", "dha"],
        "ड": ["da", "dha", "ta"],
        "ढ": ["dha", "da", "bha"],
        "ण": ["na", "nha", "na"],

        "त": ["ta", "tha", "da"],
        "थ": ["tha", "ta", "dha"],
        "द": ["da", "ta", "dha"],
        "ध": ["dha", "da", "bha"],
        "न": ["na", "pa", "ka"],

        "प": ["pa", "na", "ka"],
        "फ": ["pha", "fa", "pa"],
        "ब": ["ba", "pa", "va"],
        "भ": ["bha", "ba", "ma"],
        "म": ["ma", "na", "ba"],

        "य": ["ya", "ja", "ra"],
        "र": ["ra", "la", "na"],
        "ल": ["la", "ra", "va"],
        "व": ["va", "ba", "wa"],

        "श": ["sha", "sa", "cha"],
        "ष": ["sha", "sa", "ka"],
        "स": ["sa", "sha", "ta"],
        "ह": ["ha", "ka", "na"],

        "क्ष": ["ksha", "tra", "jna"],
        "त्र": ["tra", "ksha", "sha"],
        "ज्ञ": ["gya", "jna", "kya"]
    }
    
    try:
        # Get the current question
        current_q = session['game_data']['current_question']
        character = session['game_data']['questions'][current_q]
        options = characters[character]
        
        return render_template('game.html', 
                            character=character, 
                            options=options, 
                            lives=session['game_data']['lives'],
                            question_number=current_q + 1,
                            total_questions=session['game_data']['total_questions'])
    except Exception as e:
        # If any error occurs, reset the game session
        session.pop('game_data', None)
        return redirect(url_for('game'))

from flask import Response
from gtts import gTTS
import tempfile

@app.route('/play_sound', methods=['POST'])
def play_sound():
    try:
        data = request.get_json()
        character = data.get('character')

        if not character:
            return "Character not provided", 400

        # Generate temporary MP3 using gTTS
        tts = gTTS(text=character, lang='hi')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
            tts.save(temp_path)

        # Read file content
        with open(temp_path, 'rb') as f:
            audio_data = f.read()

        os.remove(temp_path)  # Delete the temp file immediately

        return Response(audio_data, mimetype='audio/mpeg')

    except Exception as e:
        return f"Error generating audio: {str(e)}", 500


@app.route('/game_results')
def game_results():
    if 'final_results' not in session:
        return redirect(url_for('game'))
    
    # Get the results from the session
    results = session['final_results']
    
    # Clear the results after displaying
    session.pop('final_results', None)
    
    return render_template('game_results.html',
                         score=results['score'],
                         total_questions=results['total_questions'],
                         accuracy=results['accuracy'],
                         incorrect_answers=results.get('incorrect_answers', []))
    
    
    # Clear the game data for the next game
    session.pop('game_data', None)
    session.modified = True
    
    return render_template('game_results.html', **results)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    if 'game_data' not in session or 'current_question' not in session['game_data']:
        return jsonify({'error': 'Game session not found'}), 400

    data = request.get_json()
    character = data.get('character')
    answer = data.get('answer')

    correct_answers = {
        "अ": "a",    "आ": "aa",   "इ": "i",    "ई": "ee",
        "उ": "u",    "ऊ": "oo",   "ऋ": "ri",   "ए": "e",
        "ऐ": "ai",   "ओ": "o",    "औ": "au",   "अं": "an",  "अः": "aha",
        "क": "ka",   "ख": "kha",  "ग": "ga",   "घ": "gha", "ङ": "nga",
        "च": "cha",  "छ": "chha", "ज": "ja",   "झ": "jha", "ञ": "nya",
        "ट": "ta",   "ठ": "tha",  "ड": "da",   "ढ": "dha", "ण": "na",
        "त": "ta",   "थ": "tha",  "द": "da",   "ध": "dha", "न": "na",
        "प": "pa",   "फ": "pha",  "ब": "ba",   "भ": "bha", "म": "ma",
        "य": "ya",   "र": "ra",   "ल": "la",   "व": "va",
        "श": "sha",  "ष": "sha",  "स": "sa",   "ह": "ha",
        "क्ष": "ksha", "त्र": "tra", "ज्ञ": "gya"
    }

    is_correct = answer == correct_answers.get(character)

    if not is_correct:
        session['game_data']['lives'] -= 1
        # Track incorrect answers
        session['game_data']['incorrect_answers'].append({
            'character': character,
            'user_answer': answer,
            'correct_answer': correct_answers.get(character)
        })
    else:
        session['game_data']['score'] += 1

    # Move to next question
    session['game_data']['current_question'] += 1
    # Explicitly mark the session as modified
    session.modified = True
    
    # Check if game is over
    game_over = (session['game_data']['lives'] <= 0 or 
                 session['game_data']['current_question'] >= session['game_data']['total_questions'])

    if game_over:
        accuracy = (session['game_data']['score'] / session['game_data']['total_questions']) * 100
        # Store final results in session for the results page
        session['final_results'] = {
            'score': session['game_data']['score'],
            'total_questions': session['game_data']['total_questions'],
            'accuracy': accuracy,
            'incorrect_answers': session['game_data']['incorrect_answers']
        }
        # Clear the game data for next game
        session.pop('game_data', None)
        # Return response with redirect URL
        return jsonify({
            'correct': is_correct,
            'game_over': True,
            'redirect_url': url_for('game_results')
        })

    return jsonify({
        'correct': is_correct,
        'lives': session['game_data']['lives'],
        'score': session['game_data']['score'],
        'game_over': False,
        'next_question': True
    })