import unittest
from app import app, db
from app.models import User


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


if __name__ == '__main__':
    unittest.main(verbosity=2)
