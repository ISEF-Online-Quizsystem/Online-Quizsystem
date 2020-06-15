from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Angemeldet bleiben')
    submit = SubmitField('Jetzt anmelden')


class RegistrationForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Bitte benutze einen anderen Benutzernamen.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Bitte benutze eine andere E-Mail-Adresse.')


class EditProfileForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    about_me = TextAreaField('Über mich', validators=[Length(min=0, max=140)])
    submit = SubmitField('Abschicken')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Bitte benutze einen anderen Benutzernamen.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Neues Passwort anfordern.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Fordere Passwort-Reset an')


class QuestionForm(FlaskForm):
    question = TextAreaField('Frage', validators=[Length(min=0, max=140)])
    option_one = RadioField("Antwortoption 1")
    option_two = RadioField("Antwortoption 2")
    option_three = RadioField("Antwortoption 3")
    option_four = RadioField("Antwortoption 4")
    option_five = RadioField("Antwortoption 5")
    submit = SubmitField('Frage absenden')