from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import LoginForm


@app.route('/index')
@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Anmeldung', form=form)
