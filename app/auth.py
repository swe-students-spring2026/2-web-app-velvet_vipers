from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if current_app.db.users.find_one({"email": email}):
            flash("An account with that email already exists.", "error")
            return render_template("auth/register.html")

        if current_app.db.users.find_one({"username": username}):
            flash("That username is already taken.", "error")
            return render_template("auth/register.html")

        user_doc = {
            "username": username,
            "email": email,
            "password_hash": generate_password_hash(password),
        }
        current_app.db.users.insert_one(user_doc)
        user = User(user_doc)
        login_user(user)
        return redirect(url_for("main.event_list"))

    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        doc = current_app.db.users.find_one({"email": email})
        if doc and check_password_hash(doc["password_hash"], password):
            login_user(User(doc))
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.event_list"))

        flash("Invalid email or password.", "error")

    return render_template("auth/login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.event_list"))
