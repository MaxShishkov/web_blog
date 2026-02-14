from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import pm

views = Blueprint("views", __name__, url_prefix="/")

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = pm.get_all_posts()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        post_text = request.form.get("text")
        
        if not post_text:
            flash('Post cannot be empty', category='error')
        else:
            user_id = current_user.id
            pm.create_post(user_id, post_text)
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
        
    
    return render_template("create_post.html", user=current_user)


@views.route("delete-post/<id>")
@login_required
def delete_post(id):
    try:
        pm.delete_post(id, current_user.id)
        flash('Post deleted.', category='success')
    except ValueError:
        flash("Post does not exist.", category='error')
    except PermissionError:
        flash('You do not have permission to delete this post.', category='error')
        
    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
@login_required
def posts(username):
    try:
        posts = pm.get_user_posts(username)
    except ValueError:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    
    return render_template("posts.html", user=current_user, posts=posts, username=username)