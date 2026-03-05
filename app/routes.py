from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return redirect(url_for("main.event_list"))

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if current_app.db.users.find_one({"email": email}):
            return render_template("auth/register.html", error="Email already registered.")

        doc = {
            "email": email,
            "password_hash": generate_password_hash(password),
            "plan": "free",
        }
        res = current_app.db.users.insert_one(doc)
        user = User({**doc, "_id": res.inserted_id})
        login_user(user)
        return redirect(url_for("main.event_list"))

    return render_template("auth/register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        doc = current_app.db.users.find_one({"email": email})
        if not doc or not check_password_hash(doc["password_hash"], password):
            return render_template("auth/login.html", error="Invalid email or password.")

        login_user(User(doc))
        return redirect(url_for("main.event_list"))

    return render_template("auth/login.html")


@main.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

# Screen 1: Event List

@main.route("/events")
def event_list():
    q = request.args.get("q", "").strip()
    location = request.args.get("location", "").strip()
    tag = request.args.get("tag", "").strip()

    if q or location or tag:
        and_filters = []
        if q:
            and_filters.append({"$or": [
                {"title": {"$regex": q, "$options": "i"}},
                {"description": {"$regex": q, "$options": "i"}},
            ]})
        if location:
            and_filters.append({"location": {"$regex": location, "$options": "i"}})
        if tag:
            and_filters.append({"tags": {"$elemMatch": {"$regex": tag, "$options": "i"}}})
        query = {"$and": and_filters}
    else:
        query = {}

    events = list(current_app.db.events.find(query).sort("date", 1))
    return render_template("events/list.html", events=events, q=q, location=location, tag=tag)


# Screen 2: Event Detail

@main.route("/events/<id>")
def event_detail(id):
    try:
        oid = ObjectId(id)
    except InvalidId:
        return render_template("404.html"), 404

    event = current_app.db.events.find_one({"_id": oid})
    if event is None:
        return render_template("404.html"), 404

    return render_template("events/detail.html", event=event)


# Screen 3: Create Event

@main.route("/events/new", methods=["GET", "POST"])
@login_required
def event_new():
    if request.method == "POST":
        tags_raw = request.form.get("tags", "")
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        event = {
            "title": request.form["title"],
            "location": request.form["location"],
            "date": request.form["date"],
            "tags": tags,
            "description": request.form.get("description", ""),
        }
        current_app.db.events.insert_one(event)
        return redirect(url_for("main.event_list"))
    return render_template("events/new.html")


# Screen 4: Edit Event

@main.route("/events/<id>/edit", methods=["GET", "POST"])
@login_required
def event_edit(id):
    try:
        oid = ObjectId(id)
    except InvalidId:
        return render_template("404.html"), 404

    event = current_app.db.events.find_one({"_id": oid})
    if event is None:
        return render_template("404.html"), 404

    if request.method == "POST":
        tags_raw = request.form.get("tags", "")
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        current_app.db.events.update_one(
            {"_id": oid},
            {"$set": {
                "title": request.form["title"],
                "location": request.form["location"],
                "date": request.form["date"],
                "tags": tags,
                "description": request.form.get("description", ""),
            }}
        )
        return redirect(url_for("main.event_detail", id=id))
    return render_template("events/edit.html", event=event)


# Screen 5: Delete Confirmation + Delete

@main.route("/events/<id>/delete", methods=["GET", "POST"])
@login_required
def event_delete(id):
    try:
        oid = ObjectId(id)
    except InvalidId:
        return render_template("404.html"), 404

    event = current_app.db.events.find_one({"_id": oid})
    if event is None:
        return render_template("404.html"), 404

    if request.method == "POST":
        current_app.db.events.delete_one({"_id": oid})
        return redirect(url_for("main.event_list"))
    return render_template("events/delete.html", event=event)


# Screen 6: Search 

@main.route("/search")
def search():
    q = request.args.get("q", "").strip()
    location = request.args.get("location", "").strip()
    tag = request.args.get("tag", "").strip()

    searched = any([q, location, tag])
    events = []

    if searched:
        and_filters = []
        if q:
            and_filters.append({"$or": [
                {"title": {"$regex": q, "$options": "i"}},
                {"description": {"$regex": q, "$options": "i"}},
            ]})
        if location:
            and_filters.append({"location": {"$regex": location, "$options": "i"}})
        if tag:
            and_filters.append({"tags": {"$elemMatch": {"$regex": tag, "$options": "i"}}})

        query = {"$and": and_filters} if and_filters else {}
        events = list(current_app.db.events.find(query).sort("date", 1))

    return render_template(
        "search.html",
        events=events,
        q=q,
        location=location,
        tag=tag,
        searched=searched,
    )