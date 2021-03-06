from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, \
    QuestionForm, QuestionSolve, get_modules, ModuleForm, ReleaseForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Question, Module
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email


# Mittels dieses Dekorators ist es möglich Code auszuführen bevor eine View Funktion aufgerufen wird.
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/index')
@app.route('/')
# Seite wird nur angezeigt, wenn man eingeloggt ist. Das schützt gegen anonyme Besucher.
@login_required
def index():
    tutor = False
    if current_user.tutor:
        tutor = True
    return render_template('index.html', tutor=tutor)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # überprüft, ob der Benutzer bereits eingeloggt ist.
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
    # Wenn kein Benutzer gefunden wird, dann wird ein 404 Fehler zurückgegeben.
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
    reset_status()
    if form.validate_on_submit():
        module = Module.query.filter_by(name=form.modules.data).first_or_404()
        if not module.status:
            all_module_inactive()
            module.set_status_active()
            db.session.commit()
        flash(form.modules.data + ' ausgewählt')
        return redirect(url_for('play'))
    return render_template('play.html', form=form)


def reset_status():
    module = Module.query.filter_by(status=1).first_or_404()
    questions = Question.query.filter_by(module=module.name).all()
    for q in questions:
        q.status = 0
    db.session.commit()


@app.route('/singleplayer', methods=['GET', 'POST'])
@login_required
def singleplayer():
    global right, wrong, total
    question_number = 1
    form = QuestionSolve()
    module = Module.query.filter_by(status=1).first_or_404()
    try:
        q = Question.query.filter_by(module=module.name, status=0, released=1).all()
        right = len(Question.query.filter_by(module=module.name, status=1).all())
        wrong = len(Question.query.filter_by(module=module.name, status=2).all())
        question_number = question_number + right + wrong
        if len(q) == 0 or question_number > 10:
            total = Question.query.filter_by(module=module.name, status=1).all() + Question.query.filter_by(
                module=module.name, status=2).all()
            # Die einzelnen Fragen werden in der result.html benötigt, deshalb werden sie via
            # expunge aus der Session entfernt.
            for item in total:
                db.session.expunge(item)
            reset_status()
            return redirect(url_for('result', total))
        form.radio.label.text = q[0].question
        form.radio.choices = [('1', q[0].option_one), ('2', q[0].option_two),
                              ('3', q[0].option_three),
                              ('4', q[0].option_four)]
        if form.validate_on_submit():
            if form.radio.data:
                if q[0].right_choice == int(form.radio.data):
                    #flash('Richtig')
                    q[0].status = 1
                    current_user.score = current_user.score + 1
                    current_user.number_of_questions = current_user.number_of_questions + 1
                    db.session.commit()
                else:
                    #flash('Falsch')
                    q[0].status = 2
                    current_user.number_of_questions = current_user.number_of_questions + 1
                    db.session.commit()

            if form.report.data:
                flash('Frage wurde dem Tutor gemeldet.')
                q[0].released = 0
                db.session.commit()

            return redirect(url_for('singleplayer'))

    except:
        return redirect(url_for('result'))

    return render_template('singleplayer.html', question=q, form=form, question_number=question_number)


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
    user = User.query.filter_by(tutor=0).all()
    user.sort(key=lambda x: x.score, reverse=True)
    return render_template('highscore.html', user=user)


@app.route('/result')
@login_required
def result():
    return render_template('result.html', right=right, wrong=wrong, score=current_user.score, total=total)


@app.route('/release', methods=['GET', 'POST'])
@login_required
def release():
    form = ReleaseForm()
    try:
        q = Question.query.filter_by(released=0).all()
        if len(q) == 0:
            flash('Keine Fragen zum Freigeben vorhanden.')
            return redirect(url_for('index'))
        form.module.data = q[0].module
        form.question.data = q[0].question
        form.option_one.data = q[0].option_one
        form.option_two.data = q[0].option_two
        form.option_three.data = q[0].option_three
        form.option_four.data = q[0].option_four
        form.right_choice.data = q[0].right_choice

        if form.validate_on_submit():
            if form.release.data:
                flash('Frage wurde aktualisiert.')
                q[0].module = form.module.raw_data[0]
                q[0].question = form.question.raw_data[0]
                q[0].option_one = form.option_one.raw_data[0]
                q[0].option_two = form.option_two.raw_data[0]
                q[0].option_three = form.option_three.raw_data[0]
                q[0].option_four = form.option_four.raw_data[0]
                q[0].right_choice = form.right_choice.raw_data[0]
                q[0].released = 1
                db.session.commit()
            if form.deny.data:
                flash('Frage abgelehnt')
                q[0].released = 2
                db.session.commit()

            return redirect(url_for('release'))

    except:
        return redirect(url_for('index'))

    return render_template('release.html', form=form)
