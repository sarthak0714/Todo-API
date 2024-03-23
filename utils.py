from flask_jwt_extended import create_access_token, decode_token
from flask import current_app
from datetime import datetime, timedelta
import jwt
from email_validator import validate_email, EmailNotValidError
from flask import jsonify


def generate_jwt_token(user_id):
    """Generates a JWT token for user"""
    try:
        acess_token = create_access_token(
            identity=user_id,
            expires_delta=timedelta(
                seconds=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
            ),
        )
        return acess_token
    except Exception as e:
        return str(e)


def decode_jwt_token(token):
    """Decode JWT Token and return payload"""
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        return "Token Expired, Login again."
    except jwt.InvalidTokenError:
        return "Token is Invalid, Login again."


def validate_user_registration(data):
    """
    Validates user registration data.
    """
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    try:
        # Validate.
        valid = validate_email(email)

        # Update with the normalized form.
        email = valid.email
    except EmailNotValidError as e:
        # Email is not valid, exception message is human-readable
        return jsonify({"error": str(e)}), 400

    return None


def validate_todo_data(data):
    """
    Validates todo item data.
    """
    title = data.get("title")
    status = data.get("status")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    if status is not None and not isinstance(status, bool):
        return jsonify({"error": "Status must be a boolean"}), 400

    return None


def validate_login_data(data):
    """
    Validates login data.
    """
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    return None
