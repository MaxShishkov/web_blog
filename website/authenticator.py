from argon2 import PasswordHasher
from . import db
from .models import User
from sqlalchemy import select, exists
from flask_login import login_user
from sqlalchemy.exc import IntegrityError

class Authenticator():
    def __init__(self):
        self.ph = PasswordHasher()
        
    def _hash_password(self, password: str) -> str:
        return self.ph.hash(password)
    
    
    def _get_user_hash(self, email: str) -> str | None:
        user = db.session.scalar(
            select(User).where(User.email == email)
        )
        
        return user.password if user else None
    
    def _update_user_hash(self, email: str, new_hash: str) -> None:
        if not new_hash or not isinstance(new_hash, str):
            raise ValueError("Invalide password hash")
        
        user = self.get_user(email)
        
        print("User object:", user)
        if user:
            print("User id:", user.id)
            print("Password repr:", repr(user.password))
        
        if not user:
            return False
        
        user.password = new_hash
        db.session.commit()
        return True
        
    def get_user(self, email):
        user = db.session.scalar(
            select(User).where(User.email == email)
        )
        return user
    
    def create_user(self, email: str, username: str, password: str) -> None:
        hashed = self._hash_password(password)
        user = User(
            email = email,
            username = username,
            password = hashed
        )
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
        except IntegrityError as e:
            db.session.rollback()
            print("Insert failed:", e)
        

    
    def username_exist(self, username):
        return db.session.scalar(
            select(exists().where(User.username == username))
        )
        
    def email_exist(self, email: str) -> bool:
        return db.session.scalar(
            select(exists().where(User.email == email))
        )
        
    def verify_password(self, stored_hash: str, password: str) -> bool | str:
        try:
            self.ph.verify(stored_hash, password)
        except Exception:
            return False
        
        if self.ph.check_needs_rehash(stored_hash):
            return self._hash_password(password)
        
        return True
    
    def login(self, email: str, password: str) -> bool:
        if not self.email_exist:
            print("email doesnt exist")
            return False
        
        stored_hash = self._get_user_hash(email)
        if not stored_hash:
            print("no stored hash")
            return False
        
        result = self.verify_password(stored_hash, password)
        if not result:
            print("couldnt verify")
            return False
        
        if isinstance(result, str):
            try:
                self._update_user_hash(email, result)
            except Exception:
                print("pasword update failed")
        
        user = self.get_user(email)
        if not user:
            print("couldnt get user")
            return False
        
        login_user(user, remember=True)
        return True