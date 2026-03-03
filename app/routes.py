from flask import Blueprint, render_template, request, redirect, url_for, current_app
from bson.objectid import ObjectId
from bson.errors import InvalidId

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return redirect(url_for("main.event_list"))


# Screen 1: Event List

@main.route("/events")
def event_list():
    events = list(current_app.db.events.find().sort("date", 1))
    return render_template("events/list.html", events=events)


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