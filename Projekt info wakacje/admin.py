from user import User

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin", [
            "manage_users","manage_permissions","manage_inventory","rent_cars","manage_finances"
        ])
