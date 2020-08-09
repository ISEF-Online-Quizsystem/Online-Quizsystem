import unittest
from app import app, db
from app.models import User, Question, Module


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='tobias')
        u.set_password('tutor')
        self.assertFalse(u.check_password('student'))
        self.assertTrue(u.check_password('tutor'))

    def test_avatar(self):
        u = User(username='heino', email='heino@db.de')
        self.assertEqual(u.avatar(80),
                         'https://www.gravatar.com/avatar/0b96ea15f14649137616ed50273a66cc?d=identicon&s=80')


class ModuleModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_default_status(self):
        m = Module(name='Testmodul')
        self.assertEqual(m.status, None)

    def test_status_active(self):
        m = Module(name='Aktives Modul')
        m.set_status_active()
        self.assertEqual(m.status, 1)

    def test_status_inactive(self):
        m = Module(name="Inaktives Modul")
        m.set_status_inactive()
        self.assertEqual(m.status, 0)


class QuestionModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_default_status(self):
        q = Question(question='Frage?', module='Testmodul', option_one='eins', option_two='zwei', option_three='drei',
                     option_four='vier', right_choice=2)
        self.assertEqual(q.status, None)

    def test_default_released(self):
        q = Question(question='Frage?', module='Testmodul', option_one='eins', option_two='zwei', option_three='drei',
                     option_four='vier', right_choice=2)
        self.assertEqual(q.released, None)

    def test_create_question(self):
        q = Question(question='Frage?', module='Testmodul', option_one='eins', option_two='zwei', option_three='drei',
                     option_four='vier', right_choice=2, status=1, released=1)
        self.assertEqual(q.question, 'Frage?')
        self.assertEqual(q.module, 'Testmodul')
        self.assertEqual(q.option_one, 'eins')
        self.assertEqual(q.option_two, 'zwei')
        self.assertEqual(q.option_three, 'drei')
        self.assertEqual(q.option_four, 'vier')
        self.assertEqual(q.right_choice, 2)
        self.assertEqual(q.status, 1)
        self.assertEqual(q.released, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
