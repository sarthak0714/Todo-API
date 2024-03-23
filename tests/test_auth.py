import unittest
from flask import Flask
from models import db, User
from auth import auth as auth_blueprint
from config import TestConfig
from index import create_app


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class=TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.populate_db()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def populate_db(self):
        user1 = User(username="testuser", email="test@example.com")
        user1.set_password("testpassword")
        db.session.add(user1)
        db.session.commit()

    def test_login_success(self):
        response = self.client.post(
            "/login", json={"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_login_failure(self):
        response = self.client.post(
            "/login", json={"username": "wronguser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Invalid Username or Password")


if __name__ == "__main__":
    unittest.main()
