from flask import render_template, url_for
from app import app
from app.forms import LoginForm


@app.route('/index')
@app.route('/')
def hello_world():
    member = ['Christine Rasche', 'Rubens Romanello', 'Viet-Hung Dinh', 'Andreas Gropp']
    return render_template('index.html', member=member)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
