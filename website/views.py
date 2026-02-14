from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

views = Blueprint("views", __name__, url_prefix="/")

@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("home.html", name=current_user.username)

@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        pass
    
    return render_template("create_post.html")