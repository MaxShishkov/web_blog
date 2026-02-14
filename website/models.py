from datetime import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

MAX_STR_LEN = 50

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(MAX_STR_LEN), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(MAX_STR_LEN), unique=True)
    password: Mapped[str] = mapped_column(String(MAX_STR_LEN), nullable=False)
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False
    )
    posts = db.relationship("Post", backref='user', passive_deletes=True)
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(), nullable=False)
    date_created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False
    )
    author: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )
    