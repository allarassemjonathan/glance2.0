class student:
    def __init__(self, name, year, town, state, email, box_number, room):
        self.name = name
        self.year = year
        self.town = town
        self.state = state
        self.email = email
        self.box_number=box_number
        self.room = room
        
    def __str__(self):
        return f"{self.name} {self.year} {self.email}"

        