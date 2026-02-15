from . import db
from .models import User, Post, Comment, Like
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError


class PostManager():
    def create_post(self, user_id: int, text: str ):
        new_post = Post(
            text = text,
            author = user_id
        )
        
        try:
            db.session.add(new_post)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print("Insert failed:", e)
            
    
    def get_all_posts(self) -> list[Post]:
        posts = db.session.scalars(select(Post)).all()
        return posts


    def get_user_posts(self, username):
        user = db.session.scalar(select(User).where(User.username == username))
        
        if not user:
            raise ValueError("User doesn't exist")
        
        posts = user.posts
        return posts


    def get_post_by_id(self, id: int) -> Post:
        post = db.session.scalar(select(Post).where(Post.id == id))
        return post


    def delete_post(self, post_id: int, user_id: int):
        rm_post = self.get_post_by_id(post_id)
        if not rm_post:
            raise ValueError("Post doesn't exist")
        
        if rm_post.author != user_id:
            raise PermissionError("You don't have permission to delete this post")
        
        try:
            db.session.delete(rm_post)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print("delete failed:", e)


    def create_comment(self, text, user_id, post_id):
        post = db.session.scalar(select(Post).where(Post.id == post_id))
        
        if not post:
            raise ValueError("Post doesn't exist")
        
        comment = Comment(
            text = text,
            author = user_id,
            post_id = post_id
        )
        
        try:
            db.session.add(comment)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print("Insert failed:", e)
            
            
    def delete_comment(self, comment_id, user_id):
        comment = db.session.scalar(select(Comment).where(Comment.id == comment_id))
        
        if not comment:
            raise ValueError("Comment doesn't exist")
        
        if user_id != comment.author and user_id != comment.post.author:
            raise PermissionError("You donnot have permission to delete the comment")
        
        try:
            db.session.delete(comment)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print("Delete failed:", e)


    def toggle_like_on_post(self, user_id, post_id):
        like = db.session.scalar(
            select(Like).where(
                Like.author == user_id,
                Like.post_id == post_id
            )
        )
        
        try:
            if like:
                db.session.delete(like)
                db.session.commit()
            else:
                like = Like(author = user_id, post_id = post_id)
                db.session.add(like)
                db.session.commit()
                
        except IntegrityError as e:
            db.session.rollback()
            print("Toggle on like failed:", e)