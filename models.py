from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    known_language = db.Column(db.String(50))
    target_language = db.Column(db.String(50))
    level = db.Column(db.String(20))

    def __repr__(self):
        return f'<User {self.username}>'
