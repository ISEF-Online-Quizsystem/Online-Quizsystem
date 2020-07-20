from flask import render_template, url_for, flash, redirect, request, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, \
    QuestionForm, QuestionSolve, get_modules, ModuleForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Question, Module
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/index')
@app.route('/')
@login_required
def index():
    tutor = False
    if current_user.tutor:
        tutor = True
    return render_template('index.html', tutor=tutor)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ungültiger Benutzername oder Passwort.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Anmeldung', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Gratulation, du bist jetzt registriert.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrieren', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Änderungen gespeichert')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Profil bearbeiten', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('E-Mail zur Passwortrücksetzung verschickt.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Passwortrücksetzung', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Dein Passwort wurde zurückgesetzt.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


def all_module_inactive():
    modules = Module.query.filter_by().all()
    for module in modules:
        module.status = False


@app.route('/play', methods=['GET', 'POST'])
@login_required
def play():
    form = ModuleForm()
    if form.validate_on_submit():
        module = Module.query.filter_by(name=form.modules.data).first_or_404()
        if not module.status:
            all_module_inactive()
            module.set_status_active()
            db.session.commit()
        flash(form.modules.data + ' ausgewählt')
        return redirect(url_for('play'))
    return render_template('play.html', form=form)


@app.route('/singleplayer', methods=['GET', 'POST'])
@login_required
def singleplayer():
    form = QuestionSolve()
    module = Module.query.filter_by(status=1).first_or_404()
    # question = Question.query.filter_by(module=module.name).all()
    # for q in question:
    #     form.radio.label.text = q[0].question
    #     form.radio.choices = [('1', q[0].option_one), ('2', q[0].option_two),
    #                           ('3', q[0].option_three),
    #                           ('4', q[0].option_four)]
    try:
        q = Question.query.filter_by(module=module.name).all()
        form.radio.label.text = q[0].question
        form.radio.choices = [('1', q[0].option_one), ('2', q[0].option_two),
                              ('3', q[0].option_three),
                              ('4', q[0].option_four)]
        if form.validate_on_submit():
            if q[0].right_choice == int(form.radio.data):
                flash('Richtig')
            else:
                flash('Falsch')
            return redirect(url_for('singleplayer'))
    except:
        return render_template('noquestion.html')

    return render_template('singleplayer.html', question=q, form=form)


@app.route('/multiplayer', methods=['GET', 'POST'])
@login_required
def multiplayer():
    result = get_modules()

    return render_template('multiplayer.html', result=result)


@app.route('/questions', methods=['GET', 'POST'])
@login_required
def questions():
    form = QuestionForm()
    if form.validate_on_submit():
        new_question = Question(question=form.question.data, module=form.modules.data,
                                option_one=form.option_one.data, option_two=form.option_two.data,
                                option_three=form.option_three.data, option_four=form.option_four.data,
                                right_choice=form.right_choice.data)
        db.session.add(new_question)
        db.session.commit()
        flash('Die Frage wurde eingereicht.')
        flash('Sie muss noch von einem Tutor freigegeben werden.')
        return redirect(url_for('questions'))
    return render_template('questions.html', form=form)


@app.route('/highscore', methods=['GET', 'POST'])
@login_required
def highscore():
    return render_template('highscore.html')
