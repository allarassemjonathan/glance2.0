class student:
    def __init__(self, name, year, town, state, email):
        self.name = name
        self.year = year
        self.town = town
        self.state = state
        self.email = email
        
    def __str__(self):
        return f"{self.name} {self.year} {self.email}"

        