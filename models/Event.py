

class Event():
    table = "event"
    
    def __init__(self, id, user_id, name, description, date, location):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.date = date
        self.location = location
