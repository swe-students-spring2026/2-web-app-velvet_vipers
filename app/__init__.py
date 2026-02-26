import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)

    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    db_name = os.getenv("DB_NAME", "campus_events_db")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    client = MongoClient(mongo_uri)
    app.db = client[db_name]

    app.mongo_client = client

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

    return app