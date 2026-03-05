import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_login import LoginManager
from bson.objectid import ObjectId

login_manager = LoginManager()

from .models import User

def create_app():
    load_dotenv()

    app = Flask(__name__)

    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("DB_NAME", "campus_events_db")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    client = MongoClient(mongo_uri)
    app.db = client[db_name]
    app.mongo_client = client

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        doc = app.db.users.find_one({"_id": ObjectId(user_id)})
        return User(doc) if doc else None

    @app.template_filter("format_date")
    def format_date(value):
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(value)
            return dt.strftime("%b %d, %Y at %I:%M %p")
        except Exception:
            return value

    from app.routes import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth)

    return app
