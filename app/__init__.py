from flask import Flask
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    # Initialize database
    init_db(app)

    return app
