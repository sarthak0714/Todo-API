# Todo API 

## Description
This project is a Flask-based REST API for managing todo items. It supports user authentication and allows users to create, update, delete, and search for todo items. Each todo item can have a title, description, and a status indicating whether it is completed. The project uses JWT for authentication, SQLAlchemy for ORM, ratelimiting, and includes unit tests for testing the API endpoints.

## Setting Up

### Prerequisites
- Python 3.x
- pip
- virtualenv (optional)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sarthak0714/Todo-API.git
   cd Todo-API
   ```

2. **Create and activate a virtual environment (optional):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add the following variables:
   ```plaintext
   SECRET_KEY=your_secret_key
   DATABASE_URI=your_database_uri
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

5. **Initialize the database:**
   ```bash
   flask db upgrade
   ```

6. **Run the application:**
   ```bash
   flask run
   ```

## Using the API

### Authentication

- **Register a new user:**
  ```http
  POST /register
  ```
  Body:
  ```json
  {
    "username": "your_username",
    "password": "your_password",
    "email": "your_email"
  }
  ```

- **Login:**
  ```http
  POST /login
  ```
  Body:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

### Todo Items

- **Create a new todo:**
  ```http
  POST /create
  ```
  Headers:
  ```plaintext
  Authorization: Bearer <your_jwt_token>
  ```
  Body:
  ```json
  {
    "title": "Todo Title",
    "description": "Todo Description",
    "status": false
  }
  ```

- **Get all todos:**
  ```http
  GET /todos
  ```
  Headers:
  ```plaintext
  Authorization: Bearer <your_jwt_token>
  ```

- **Update a todo:**
  ```http
  PUT /update/<todo_id>
  ```
  Headers:
  ```plaintext
  Authorization: Bearer <your_jwt_token>
  ```
  Body:
  ```json
  {
    "title": "Updated Title",
    "description": "Updated Description",
    "status": true
  }
  ```

- **Delete a todo:**
  ```http
  DELETE /delete/<todo_id>
  ```
  Headers:
  ```plaintext
  Authorization: Bearer <your_jwt_token>
  ```

- **Search todos:**
  ```http
  GET /search
  ```
  Headers:
  ```plaintext
  Authorization: Bearer <your_jwt_token>
  ```
  Body:
  ```json
  {
    "title": "Search Title",
    "description": "Search Description",
    "status": true
  }
  ```

### Running Tests

To run the unit tests, execute the following command:
```bash
python -m unittest discover ./tests/
```

This project provides a comprehensive API for managing todo items with user authentication, making it a versatile tool for todo list applications.
