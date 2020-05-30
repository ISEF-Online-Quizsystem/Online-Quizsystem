from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


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

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.String(64), index=True)
    question = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    answers = db.relationship('Answer', lazy='dynamic')

    def __repr__(self):
        return f'<Question {self.question}>'


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_one = db.Column(db.String(64))
    option_two = db.Column(db.String(64))
    option_three = db.Column(db.String(64))
    option_four = db.Column(db.String(64))
    option_five = db.Column(db.String(64))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
