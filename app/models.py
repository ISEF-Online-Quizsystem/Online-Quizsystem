from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt
from app import app

# Ladet den eingeloggten Benutzer aus der Datenbank
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    tutor = db.Column(db.Boolean, default=0)
    score = db.Column(db.Integer, default=0)
    number_of_questions = db.Column(db.Integer, default=0)

    # Diese Methode zeigt die Objekte dieser Klasse an. Das ist nützlich für das Debugging.
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Generiert ein Avatar-Bild mit Hilfe der E-Mail-Adresse und eines MD5 Hash
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    # Generiert ein JSON Web Token
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    module = db.Column(db.String(128))
    option_one = db.Column(db.String(256))
    option_two = db.Column(db.String(256))
    option_three = db.Column(db.String(256))
    option_four = db.Column(db.String(256))
    right_choice = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)
    released = db.Column(db.Integer, default=0)

    # Diese Methode zeigt die Objekte dieser Klasse an. Das ist nützlich für das Debugging.
    def __repr__(self):
        return f'<Question {self.question}>'


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    status = db.Column(db.Boolean, default=0)

    # Diese Methode zeigt die Objekte dieser Klasse an. Das ist nützlich für das Debugging.
    def __repr__(self):
        return f'<Module {self.name}>'

    def set_status_active(self):
        self.status = 1

    def set_status_inactive(self):
        self.status = 0
