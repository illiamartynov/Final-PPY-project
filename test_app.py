import unittest
from app import app, db
from app.models import Message
from datetime import datetime


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_message(self):
        response = self.app.post('/', data=dict(
            user='TestUser',
            message='This is a test message'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestUser', response.data)
        self.assertIn(b'This is a test message', response.data)

    def test_get_messages(self):
        # Тест получения всех сообщений
        with app.app_context():
            msg1 = Message(user='User1', message='Message 1', timestamp=datetime.utcnow())
            msg2 = Message(user='User2', message='Message 2', timestamp=datetime.utcnow())
            db.session.add(msg1)
            db.session.add(msg2)
            db.session.commit()

        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User1', response.data)
        self.assertIn(b'Message 1', response.data)
        self.assertIn(b'User2', response.data)
        self.assertIn(b'Message 2', response.data)

    def test_timestamp(self):
        with app.app_context():
            msg = Message(user='TestUser', message='Test message', timestamp=datetime(2022, 1, 1, 12, 0, 0))
            db.session.add(msg)
            db.session.commit()

        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestUser', response.data)
        self.assertIn(b'Test message', response.data)
        self.assertIn(b'2022-01-01 12:00:00', response.data)


if __name__ == '__main__':
    unittest.main()
