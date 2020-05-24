from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/index')
@app.route('/')
def hello_world():
    member = ['Christine Rasche', 'Rubens Romanello', 'Viet-Hung Dinh', 'Andreas Gropp']
    return render_template('index.html', member=member)
