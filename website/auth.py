from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import logout_user, current_user, login_required
from . import db
from . import authy
from . import validator

auth = Blueprint("auth", __name__, url_prefix="/")

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        if authy.login(email, password):
            flash("Logged In!", category="success")
            return redirect(url_for("views.home"))
        else:
            flash("User name or password don't match!", category="error")
        
    return render_template("login.html")

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password1")
        password2 =  request.form.get("password2")
        email = request.form.get("email")
        
        if not validator.validate_email(email):
            flash("Email is not a valid email address.", category="error")   
        elif authy.email_exist(email):
            flash("Email is already in use.", category="error")
        elif authy.username_exist(username):
            flash("User name is already in use.", category="error")  
        elif password != password2:
            flash("Passwords don't match!", category="error")
        else:
            authy.create_user(email, username, password)
            flash("User created!")
            return redirect(url_for('views.home'))
    
    return render_template("signup.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
