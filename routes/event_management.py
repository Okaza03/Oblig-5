from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import logout_user, login_required, login_user
from database import DataBase
from models.Event import Event

event_bp = Blueprint("events", __name__)  


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

    return render_template("event/create-event.html")
