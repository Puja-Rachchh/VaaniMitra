from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import secrets

app = Flask(__name__)
#secret_key = secrets.token_hex(16) # Generates a 32-character hexadecimal string
app.secret_key = 'fkeifhei46ngjrn'

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import routes after creating app and db to avoid circular imports
from routes import *
from game_routes import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
