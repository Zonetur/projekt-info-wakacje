class User:
    def __init__(self, username, password, role, permissions=None):
        self.username = username
        self.password = password
        self.role = role
        self.permissions = permissions or []

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "permissions": self.permissions,
        }

    @staticmethod
    def from_dict(d):
        return User(d["username"], d["password"], d["role"], d.get("permissions", []))
