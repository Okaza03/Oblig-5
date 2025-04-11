import os
from database import DataBase
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


def register_users_to_events(num_registrations=80):
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
        DataBase(User).createIfNotExists(User(None, u['firstName'], u['lastName'], u['email'], u['password']))

    for e in events:
        DataBase(Event).createIfNotExists(Event(None, e['user_id'], e['name'], e['description'], e['date'], e['location']))

    # for r in registrations:
    #     f.write(
    #         f"INSERT INTO event_has_user (user_id, event_id) "
    #         f"VALUES ({r['user_id']}, {r['event_id']});\n"
    #     )

    print(f"\n✅ Data generated successfully!")


# Run
create_users()
create_events()
register_users_to_events()
export_to_sql_file()
