from app import app, db
from app.models import User, Question

# Diese Funktion kreiert einen Shell Context und fügt dabei die Datenbank-Instanz und die Modelle in die Shell Sitzung.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Question': Question}

