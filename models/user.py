from flask_login import UserMixin


class User(UserMixin):
    table = "user"
    
    def __init__(self, id, firstName, lastName, email):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
