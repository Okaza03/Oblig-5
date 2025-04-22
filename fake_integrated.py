from database import DataBase
from DataBaseConnection import DataBaseConnection
from faker import Faker
from werkzeug.security import generate_password_hash
import random
from datetime import datetime

from models.Event import Event
from models.User import User

fake = Faker("no_NO")

# Simulated "database" tables
users = []
events = []
registrations = []

# Auto-increment counters
user_id_counter = 1
event_id_counter = 1


def create_users(n=50):
    global user_id_counter
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@gmail.com"
        password = generate_password_hash("test")

        user = {
            "id": user_id_counter,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password,
        }

        users.append(user)
        user_id_counter += 1


def create_events(n=15):
    global event_id_counter
    for _ in range(n):
        user = random.choice(users)  # Event owner
        name = fake.company().replace("'", "''")
        description = fake.sentence().replace("'", "''")
        date = fake.date_between(start_date="today", end_date="+30d")
        time = fake.time()

        # Combine date and time
        date_time_str = f"{date} {time}"
        date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        location = fake.location_on_land(coords_only=False)

        event = {
            "id": event_id_counter,
            "user_id": user["id"],
            "name": name,
            "description": description,
            "date": date_time_obj.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # Final formatted datetime
            "location": f"{location[2]}, {location[3]}",
        }

        events.append(event)
        event_id_counter += 1


def register_users_to_events(num_registrations=200):
    for _ in range(num_registrations):
        user = random.choice(users)
        event = random.choice(events)

        already_registered = any(
            reg["user_id"] == user["id"] and reg["event_id"] == event["id"]
            for reg in registrations
        )

        if already_registered:
            continue

        registrations.append({"user_id": user["id"], "event_id": event["id"]})


def export_to_sql_file():
    for u in users:
        user_model = User(
            None, u["firstName"], u["lastName"], u["email"], u["password"]
        )
        created_user = DataBase(User).createIfNotExists(user_model)
        u["db_id"] = created_user.id

    for e in events:
        db_user_id = next(u["db_id"] for u in users if u["id"] == e["user_id"])
        event_model = Event(
            None, db_user_id, e["name"], e["description"], e["date"], e["location"]
        )
        created_event = DataBase(Event).createIfNotExists(event_model)
        e["db_id"] = created_event.id  # lagre faktisk event-ID også

    with DataBaseConnection() as db:
        for r in registrations:
            db_user_id = next(u["db_id"] for u in users if u["id"] == r["user_id"])
            db_event_id = next(e["db_id"] for e in events if e["id"] == r["event_id"])
            db.cursor.execute(
                "INSERT INTO event_has_user (user_id, event_id) VALUES (%s, %s)",
                (db_user_id, db_event_id),
            )

    print(f"\n✅ Data generated successfully!")


# Run
create_users()
create_events()
register_users_to_events()
export_to_sql_file()
