from flask import jsonify, request, Blueprint
from models import db, Todo, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import validate_todo_data

todo = Blueprint("todo", __name__)


@todo.route("/create", methods=["POST"])
@jwt_required()
def create_todo():
    """Create a new todo"""
    user_id = get_jwt_identity()
    data = request.get_json()

    err = validate_todo_data(data)
    if err:
        return err

    title = data.get("title")
    description = data.get("description")
    status = data.get("status", False)
    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_todo = Todo(
        title=title, description=description, status=status, user_id=user_id
    )

    db.session.add(new_todo)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Todo item created successfully",
                "todo": {
                    "id": new_todo.id,
                    "title": new_todo.title,
                    "description": new_todo.description,
                    "status": new_todo.status,
                    "created_at": new_todo.created_at,
                },
            }
        ),
        201,
    )


@todo.route("/todos", methods=["GET"])
@jwt_required()
def get_todos():
    """Get all todos for the logged-in user"""
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id)
    output = []
    for todo in todos:
        todo_data = {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "status": todo.status,
            "created_at": todo.created_at,
        }
        output.append(todo_data)
    return jsonify({"todos": output}), 200


@todo.route("/update/<todo_id>", methods=["PUT"])
@jwt_required()
def update_todo(todo_id: int):
    """Update the todo"""
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json()
    todo.title = data.get("title", todo.title)
    todo.description = data.get("description", todo.description)
    todo.status = data.get("status", todo.status)

    db.session.commit()

    return jsonify({"message": "Todo item updated successfully"}), 200


@todo.route("/delete/<todo_id>", methods=["DELETE"])
@jwt_required()
def delete_todo(todo_id: int):
    """Delete a todo."""
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        return jsonify({"error": "Todo item not found"}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "Todo item deleted successfully"}), 200


@todo.route("/search", methods=["GET"])
@jwt_required()
def search():
    """Search and filter Todos based to title, description and status"""
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")

    query = Todo.query.filter_by(user_id=user_id)

    if title:
        query = query.filter(Todo.title.ilike(f"%{title}%"))
    if description:
        query = query.filter(Todo.description.ilike(f"%{description}%"))

    if status is not None:
        query = query.filter(Todo.status == status)

    todos = query.all()
    output = []
    for todo in todos:
        todo_data = {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "status": todo.status,
            "created_at": todo.created_at,
        }
        output.append(todo_data)

    return jsonify({"todos": output}), 200
