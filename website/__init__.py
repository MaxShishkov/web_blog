from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, environ
from dotenv import load_dotenv
from flask_login import LoginManager
from .views import views
from .auth import auth

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
    app.register_blueprint(views)
    app.register_blueprint(auth)
    
    return app