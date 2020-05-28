from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'


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
