from flask import Blueprint, jsonify
from models.Event import Event
from models.User import User
from database import DataBase

event_api = Blueprint("event_api", __name__, url_prefix="/api/event")


@event_api.route("/<int:event_id>")
def get_event(event_id):
    db = DataBase(Event, load_with=(User, "id", "user_id"))
    event = db.firstWhere("id", event_id)

    if not event:
        return jsonify({"error": "Not found"}), 404

    return jsonify(
        {
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "date": event.date,
            "location": event.location,
            "image": event.getImage(),
            "user": {"fullName": event.user.fullName()},
        }
    )


@event_api.route("/one-from-each-user")
def get_one_event_per_user():
    db = DataBase(Event, load_with=(User, "id", "user_id"))
    all_events = db.all()

    # Create a dict keyed by user_id, first event wins
    events_by_user = {}
    for event in all_events:
        if event.user_id not in events_by_user:
            events_by_user[event.user_id] = event

    data = []
    for event in events_by_user.values():
        data.append(
            {
                "id": event.id,
                "name": event.name,
                "description": event.description,
                "date": event.date,
                "location": event.location,
                "image": event.getImage(),
                "user": {"fullName": event.user.fullName()},
            }
        )

    return jsonify(data)
