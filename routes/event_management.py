from config import (
    app,
    current_app,
    request,
    current_user,
    render_template,
    redirect,
    url_for,
    login_required,
    secure_filename,
    Blueprint,
    os,
    mail,
    Message,
)

from files import allowed_file
from database import DataBase
from models.Event import Event

app = current_app
event_bp = Blueprint("events", __name__)


@event_bp.route("/my-events")
@login_required
def my_events():
    return render_template(
        "event/my-events.html",
        my_events=DataBase(Event).Where("user_id", current_user.id),
        title="My Events",
    )


@event_bp.route("/create-event", methods=["GET", "POST"])
@login_required
def create_event():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")
        image = request.files.get("image")

        new_event = Event(
            None, current_user.id, name, description, date, location, None
        )  # Todo: id nullable

        created_event = DataBase(Event).createIfNotExists(new_event)

        if not created_event:
            return render_template(
                "event/create-event.html", error="Something went wrong"
            )

        if image:
            file = image

            if not file.filename == "":
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)

                    name_part, ext = os.path.splitext(filename)
                    custom_filename = f"event_{created_event.id}{ext}"

                    file.save(
                        os.path.join(app.config["UPLOAD_FOLDER"], custom_filename)
                    )

                    created_event.image = custom_filename

                    DataBase(Event).update(created_event)

        return redirect(url_for("events.my_events"))

    return render_template("event/create-event.html", title="Create Event")


@event_bp.route("/attending-events")
@login_required
def attending_events():
    return render_template(
        "event/attending-events.html",
        my_events=current_user.events(),
        title="Attending Events",
    )


@event_bp.route("/event/<int:event_id>", methods=["GET", "POST"])
@login_required
def info(event_id):
    db = DataBase(Event)
    current_event = db.firstWhere("id", event_id)

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            current_user.attends(current_event)
            send_confirmation_email(current_user.email, current_event.name)

        elif action == "remove":
            current_user.notAttends(current_event)

    users = current_event.users()
    attending = any(user.id == current_user.id for user in users) if users else False

    return render_template(
        "event/info.html",
        event=current_event,
        manager=current_event.manager(),
        users=users,
        attending=attending,
        title=f"{current_event.name} Info"
    )


def send_confirmation_email(user_email, event_name):
    msg = Message(
        subject="Event attendance",
        sender="eventhub_management@gmail.com",
        recipients=[user_email],
    )
    msg.html = render_template("emails/confirmation.html", event_name=event_name)

    try:
        mail.send(msg)

    except Exception as e:
        print("Error:", e)


@event_bp.route("/event/<int:event_id>/edit", methods=["POST"])
@login_required
def edit_event(event_id):
    db = DataBase(Event)
    event = db.firstWhere("id", event_id)

    if not event or event.user_id != current_user.id:
        return redirect(url_for("events.info", event_id=event_id))

    name = request.form["name"]
    description = request.form["description"]
    date = request.form["date"]
    location = request.form["location"]
    image = request.files.get("image")

    errors = []
    custom_filename = event.image

    if image:
        if image.filename != "":
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                name_part, ext = os.path.splitext(filename)
                custom_filename = f"event_{event.id}{ext}"

                image.save(os.path.join(app.config["UPLOAD_FOLDER"], custom_filename))

    updated_event = Event(
        id=event.id,
        user_id=current_user.id,
        name=name,
        description=description,
        date=date,
        location=location,
        image=custom_filename,
    )

    if not DataBase(Event).update(updated_event):
        errors.append("Something went wrong")

    return (
        redirect(url_for("events.info", event_id=event.id))
        if not errors
        else render_template(
            "event/info.html",
            event=event,
            manager=event.manager(),
            users=event.users(),
            attending=True,
            errors=errors,
            title=f"{event.name} Info",
        )
    )
