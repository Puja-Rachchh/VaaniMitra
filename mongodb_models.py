from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime
import os

mongo = PyMongo()

class User:
    def __init__(self, username=None, password=None, known_language=None, 
                 target_language=None, level=None, _id=None):
        self.username = username
        self.password = password
        self.known_language = known_language
        self.target_language = target_language
        self.level = level
        self._id = _id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        """Save user to MongoDB"""
        user_data = {
            'username': self.username,
            'password': self.password,
            'known_language': self.known_language,
            'target_language': self.target_language,
            'level': self.level,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        if self._id:
            # Update existing user
            mongo.db.users.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': user_data}
            )
        else:
            # Create new user
            result = mongo.db.users.insert_one(user_data)
            self._id = result.inserted_id
        
        return self
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches stored hash"""
        return check_password_hash(self.password, password)
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            user = User()
            user._id = user_data['_id']
            user.username = user_data['username']
            user.password = user_data['password']
            user.known_language = user_data.get('known_language')
            user.target_language = user_data.get('target_language')
            user.level = user_data.get('level')
            user.created_at = user_data.get('created_at')
            user.updated_at = user_data.get('updated_at')
            return user
        return None
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        try:
            user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            if user_data:
                user = User()
                user._id = user_data['_id']
                user.username = user_data['username']
                user.password = user_data['password']
                user.known_language = user_data.get('known_language')
                user.target_language = user_data.get('target_language')
                user.level = user_data.get('level')
                user.created_at = user_data.get('created_at')
                user.updated_at = user_data.get('updated_at')
                return user
        except Exception as e:
            # Handle invalid ObjectId or other errors
            print(f"Error finding user by ID {user_id}: {e}")
        return None
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        users = []
        for user_data in mongo.db.users.find():
            user = User()
            user._id = user_data['_id']
            user.username = user_data['username']
            user.password = user_data['password']
            user.known_language = user_data.get('known_language')
            user.target_language = user_data.get('target_language')
            user.level = user_data.get('level')
            user.created_at = user_data.get('created_at')
            user.updated_at = user_data.get('updated_at')
            users.append(user)
        return users
    
    def delete(self):
        """Delete user from database"""
        if self._id:
            mongo.db.users.delete_one({'_id': ObjectId(self._id)})
            return True
        return False
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            '_id': str(self._id) if self._id else None,
            'username': self.username,
            'known_language': self.known_language,
            'target_language': self.target_language,
            'level': self.level,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    # Flask-Login required methods
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self._id)


class UserProgress:
    """Class to handle user progress and scores"""
    
    def __init__(self, user_id=None, level=None, score=None, completed=False, _id=None):
        self.user_id = user_id
        self.level = level
        self.score = score
        self.completed = completed
        self._id = _id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        """Save progress to MongoDB"""
        progress_data = {
            'user_id': ObjectId(self.user_id),
            'level': self.level,
            'score': self.score,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        if self._id:
            # Update existing progress
            mongo.db.user_progress.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': progress_data}
            )
        else:
            # Create new progress or update existing
            existing = mongo.db.user_progress.find_one({
                'user_id': ObjectId(self.user_id),
                'level': self.level
            })
            
            if existing:
                mongo.db.user_progress.update_one(
                    {'_id': existing['_id']},
                    {'$set': progress_data}
                )
                self._id = existing['_id']
            else:
                result = mongo.db.user_progress.insert_one(progress_data)
                self._id = result.inserted_id
        
        return self
    
    @staticmethod
    def get_user_progress(user_id):
        """Get all progress for a user"""
        progress_list = []
        for progress_data in mongo.db.user_progress.find({'user_id': ObjectId(user_id)}):
            progress = UserProgress()
            progress._id = progress_data['_id']
            progress.user_id = progress_data['user_id']
            progress.level = progress_data['level']
            progress.score = progress_data['score']
            progress.completed = progress_data['completed']
            progress.created_at = progress_data.get('created_at')
            progress.updated_at = progress_data.get('updated_at')
            progress_list.append(progress)
        return progress_list
    
    @staticmethod
    def get_level_progress(user_id, level):
        """Get progress for a specific level"""
        progress_data = mongo.db.user_progress.find_one({
            'user_id': ObjectId(user_id),
            'level': level
        })
        
        if progress_data:
            progress = UserProgress()
            progress._id = progress_data['_id']
            progress.user_id = progress_data['user_id']
            progress.level = progress_data['level']
            progress.score = progress_data['score']
            progress.completed = progress_data['completed']
            progress.created_at = progress_data.get('created_at')
            progress.updated_at = progress_data.get('updated_at')
            return progress
        return None
