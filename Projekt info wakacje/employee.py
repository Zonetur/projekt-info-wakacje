from user import User

class Employee(User):
    def __init__(self, username, password, permissions=None):
        super().__init__(username, password, "employee", permissions or ["rent_cars"])
