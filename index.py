from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

import config
from models import db
from error_handlers import register_error_handlers
from auth import auth
from todo import todo
from flask_migrate import Migrate
from flask_limiter import Limiter, util


def create_app(config_class=config.Config):
    """Initalize a Flask app with given configurations"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    limiter = Limiter(
        util.get_remote_address,
        app=app,
        default_limits=["800 per day", "200 per hour"],
    )

    # Intialize extentions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)

    app.register_blueprint(auth)
    app.register_blueprint(todo)
    register_error_handlers(app)

    @app.route("/")
    def main():
        return jsonify({"message": "Todo API"})

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
