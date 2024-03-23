from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
from models import db, User
from datetime import datetime, timedelta
from utils import generate_jwt_token, decode_jwt_token
from werkzeug.security import generate_password_hash
from utils import validate_login_data

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    err = validate_login_data(data)
    if err:
        return err

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check if username or email already exists
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"message": "Email already exists"}), 400

    # Create new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    passoword = request.json.get("password")

    if not username or not passoword:
        return jsonify({"error": "Username and Password required."}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.pass_hash, passoword):
        token = generate_jwt_token(user.id)
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid Username or Password"}), 401
