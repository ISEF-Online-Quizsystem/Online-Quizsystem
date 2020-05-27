from flask import render_template, url_for
from app import app
from app.forms import LoginForm


@app.route('/index')
@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
