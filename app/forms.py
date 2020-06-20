from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange
from app.models import User, Module


def get_modules():
    modules = []
    results = Module.query.filter_by().all()
    for result in results:
        modules.append(result.name)

    return modules


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
    modules = SelectField('Wähle einen Kurs aus!', choices=get_modules())
    question = TextAreaField('Frage', validators=[Length(min=0, max=140)])
    option_one = StringField('Antwortoption 1', validators=[DataRequired()])
    option_two = StringField('Antwortoption 2', validators=[DataRequired()])
    option_three = StringField('Antwortoption 3', validators=[DataRequired()])
    option_four = StringField('Antwortoption 4', validators=[DataRequired()])
    option_five = StringField('Antwortoption 5', validators=[DataRequired()])
    right_answer = StringField('Richtige Anwort', validators=[DataRequired(), NumberRange(1, 5)])
    submit = SubmitField('Frage absenden')

