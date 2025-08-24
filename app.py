from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from mongodb_models import mongo, User
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.secret_key = os.getenv('SECRET_KEY', 'fkeifhei46ngjrn')

# Configure MongoDB
app.config['MONGO_URI'] = os.getenv('MONGODB_URI') + os.getenv('DATABASE_NAME', 'vaanimitra_db')

# Initialize MongoDB
mongo.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Specify the login route name

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.find_by_id(user_id)
    except Exception as e:
        # If user_id is invalid (e.g., from old SQLite system), return None
        print(f"Error loading user {user_id}: {e}")
        return None

# Import routes after creating app and mongo to avoid circular imports
from routes import *
from game_routes import *

if __name__ == '__main__':
    app.run(debug=True)
