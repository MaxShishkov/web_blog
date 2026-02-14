from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from os import path, environ
from dotenv import load_dotenv
from flask_login import LoginManager



class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
DB_NAME = "database.db"

from .authenticator import Authenticator
from .validator import Validator
from .postmanager import PostManager

authy = Authenticator()
validator = Validator()
pm = PostManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views)
    app.register_blueprint(auth)
    
    from .models import User, Post
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created database!")