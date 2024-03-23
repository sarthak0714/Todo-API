import unittest
from flask import Flask
from models import db, User
from todo import todo as todo_blueprint
from index import create_app
from config import TestConfig


class TestTodoBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Register a test user
        resp = self.client.post(
            "/register",
            json={"username": "test", "password": "test", "email": "test@test.com"},
        )
        self.assertEqual(resp.status_code, 201)

        # Login the test user
        resp = self.client.post("/login", json={"username": "test", "password": "test"})
        self.assertEqual(resp.status_code, 200)
        self.token = resp.get_json()["token"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_todo(self):
        with self.client as c:
            resp = c.post(
                "/create",
                headers={"Authorization": f"Bearer {self.token}"},
                json={"title": "Test Todo", "description": "desc"},
            )
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(
                resp.get_json()["message"], "Todo item created successfully"
            )

    def test_get_todos(self):
        with self.client as c:
            resp = c.get("/todos", headers={"Authorization": f"Bearer {self.token}"})
            self.assertEqual(resp.status_code, 200)

    def test_update_todo(self):
        # Create a new todo
        resp = self.client.post(
            "/create",
            json={"title": "Test Todo"},
            headers={"Authorization": f"Bearer {self.token}"},
        )
        todo_id = resp.get_json()["todo"]["id"]

        # Update the todo
        resp = self.client.put(
            f"/update/{todo_id}",
            json={"title": "Updated Test Todo"},
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["message"], "Todo item updated successfully")

    def test_delete_todo(self):
        # Create a new todo
        resp = self.client.post(
            "/create",
            json={"title": "Test Todo"},
            headers={"Authorization": f"Bearer {self.token}"},
        )
        todo_id = resp.get_json()["todo"]["id"]

        # Delete the todo
        resp = self.client.delete(
            f"/delete/{todo_id}",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["message"], "Todo item deleted successfully")

    def test_search_todos(self):
        # Create a new todo
        resp = self.client.post(
            "/create",
            json={
                "title": "Test Todo",
                "description": "Test Description",
                "status": True,
            },
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(resp.status_code, 201)

        # Search for the todo by title
        resp = self.client.get(
            "/search",
            json={"title": "Test Todo"},
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["todos"][0]["title"], "Test Todo")

        # Search for the todo by description
        resp = self.client.get(
            "/search",
            json={"description": "Test Description"},
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["todos"][0]["description"], "Test Description")

        # Search for the todo by status
        resp = self.client.get(
            "/search",
            json={"status": True},
            headers={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["todos"][0]["status"], True)


if __name__ == "__main__":
    unittest.main()
