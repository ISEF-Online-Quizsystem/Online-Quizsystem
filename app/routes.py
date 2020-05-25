from flask import render_template, url_for
from app import app


@app.route('/index')
@app.route('/')
def hello_world():
    member = ['Christine Rasche', 'Rubens Romanello', 'Viet-Hung Dinh', 'Andreas Gropp']
    return render_template('index.html', member=member)
