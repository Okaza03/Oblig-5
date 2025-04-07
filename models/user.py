from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, firstName, lastName, email):
        self.id = id
        self.firstName = lastName
        self.name = f"{firstName} {lastName}"
        self.email = email
