from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from database import DataBase
from models.Event import Event

event_bp = Blueprint("events", __name__)


@event_bp.route("/my-events")
@login_required
def my_events():
    return render_template(
        "event/my-events.html",
        my_events=DataBase(Event).Where("user_id", current_user.id),
        title="My Events",
    )


@event_bp.route("/attending-events")
@login_required
def attending_events():
    return render_template(
        "event/attending-events.html",
        my_events=DataBase(Event).Where("user_id", current_user.id),
        title="Attending Events",
    )


@event_bp.route("/event/<int:event_id>")
@login_required
def info(event_id):
    db = DataBase(Event)
    current_event = db.firstWhere("id", event_id)
    return render_template(
        "event/info.html", event=current_event, title=f"{current_event.name} Info"
    )


@event_bp.route("/create-event", methods=["GET", "POST"])
@login_required
def create_event():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")

        with DataBase(Event) as db:
            db.create_event(name, description, date, location)

        return redirect(url_for("event.my_events"))

    return render_template("event/create-event.html", title="Create Event")
