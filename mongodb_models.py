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


class MultilingualVocabulary:
    """Class to handle multilingual vocabulary storage and retrieval"""
    
    def __init__(self, category=None, key=None, english=None, translations=None, _id=None):
        self.category = category
        self.key = key
        self.english = english
        self.translations = translations or {}
        self._id = _id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        """Save multilingual vocabulary to MongoDB"""
        vocab_data = {
            'category': self.category,
            'key': self.key,
            'english': self.english,
            'translations': self.translations,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        if self._id:
            # Update existing vocabulary
            mongo.db.multilingual_vocabulary.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': vocab_data}
            )
        else:
            # Create new vocabulary or update existing
            existing = mongo.db.multilingual_vocabulary.find_one({
                'category': self.category,
                'key': self.key
            })
            
            if existing:
                mongo.db.multilingual_vocabulary.update_one(
                    {'_id': existing['_id']},
                    {'$set': vocab_data}
                )
                self._id = existing['_id']
            else:
                result = mongo.db.multilingual_vocabulary.insert_one(vocab_data)
                self._id = result.inserted_id
        
        return self
    
    def add_translation(self, language, translation):
        """Add translation for a specific language"""
        self.translations[language] = translation
        self.updated_at = datetime.utcnow()
        return self.save()
    
    def get_translation(self, language):
        """Get translation for a specific language"""
        return self.translations.get(language, self.english)
    
    @staticmethod
    def get_vocabulary_by_category(category, language='english'):
        """Get all vocabulary items for a category in specified language"""
        vocabulary = []
        for vocab_data in mongo.db.multilingual_vocabulary.find({'category': category}):
            item = {
                'key': vocab_data['key'],
                'english': vocab_data['english'],
                'translation': vocab_data['translations'].get(language, vocab_data['english']),
                'category': vocab_data['category']
            }
            vocabulary.append(item)
        return vocabulary
    
    @staticmethod
    def get_all_categories():
        """Get all available vocabulary categories"""
        categories = mongo.db.multilingual_vocabulary.distinct('category')
        return categories
    
    @staticmethod
    def get_supported_languages():
        """Get all languages that have translations"""
        languages = set(['english'])  # English is always supported
        for vocab_data in mongo.db.multilingual_vocabulary.find():
            languages.update(vocab_data.get('translations', {}).keys())
        return list(languages)
    
    @staticmethod
    def find_by_key(category, key):
        """Find vocabulary item by category and key"""
        vocab_data = mongo.db.multilingual_vocabulary.find_one({
            'category': category,
            'key': key
        })
        
        if vocab_data:
            vocab = MultilingualVocabulary()
            vocab._id = vocab_data['_id']
            vocab.category = vocab_data['category']
            vocab.key = vocab_data['key']
            vocab.english = vocab_data['english']
            vocab.translations = vocab_data.get('translations', {})
            vocab.created_at = vocab_data.get('created_at')
            vocab.updated_at = vocab_data.get('updated_at')
            return vocab
        return None
    
    @staticmethod
    def bulk_create_vocabulary(vocabulary_data):
        """Bulk create vocabulary items"""
        items_to_insert = []
        for category, items in vocabulary_data.items():
            for key, data in items.items():
                item = {
                    'category': category,
                    'key': key,
                    'english': data.get('english', key),
                    'translations': data.get('translations', {}),
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
                items_to_insert.append(item)
        
        if items_to_insert:
            result = mongo.db.multilingual_vocabulary.insert_many(items_to_insert)
            return len(result.inserted_ids)
        return 0


class UserLanguagePreference:
    """Class to handle user language preferences"""
    
    def __init__(self, user_id=None, preferred_language=None, 
                 native_language=None, learning_languages=None, _id=None):
        self.user_id = user_id
        self.preferred_language = preferred_language or 'english'
        self.native_language = native_language or 'english'
        self.learning_languages = learning_languages or []
        self._id = _id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        """Save language preferences to MongoDB"""
        pref_data = {
            'user_id': ObjectId(self.user_id),
            'preferred_language': self.preferred_language,
            'native_language': self.native_language,
            'learning_languages': self.learning_languages,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        if self._id:
            # Update existing preferences
            mongo.db.user_language_preferences.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': pref_data}
            )
        else:
            # Create new preferences or update existing
            existing = mongo.db.user_language_preferences.find_one({
                'user_id': ObjectId(self.user_id)
            })
            
            if existing:
                mongo.db.user_language_preferences.update_one(
                    {'_id': existing['_id']},
                    {'$set': pref_data}
                )
                self._id = existing['_id']
            else:
                result = mongo.db.user_language_preferences.insert_one(pref_data)
                self._id = result.inserted_id
        
        return self
    
    def add_learning_language(self, language):
        """Add a language to learning list"""
        if language not in self.learning_languages:
            self.learning_languages.append(language)
            self.updated_at = datetime.utcnow()
            return self.save()
        return self
    
    def remove_learning_language(self, language):
        """Remove a language from learning list"""
        if language in self.learning_languages:
            self.learning_languages.remove(language)
            self.updated_at = datetime.utcnow()
            return self.save()
        return self
    
    @staticmethod
    def get_user_preferences(user_id):
        """Get language preferences for a user"""
        pref_data = mongo.db.user_language_preferences.find_one({
            'user_id': ObjectId(user_id)
        })
        
        if pref_data:
            pref = UserLanguagePreference()
            pref._id = pref_data['_id']
            pref.user_id = pref_data['user_id']
            pref.preferred_language = pref_data['preferred_language']
            pref.native_language = pref_data['native_language']
            pref.learning_languages = pref_data['learning_languages']
            pref.created_at = pref_data.get('created_at')
            pref.updated_at = pref_data.get('updated_at')
            return pref
        return None


def get_database():
    """Get database instance"""
    return mongo.db
