class Auth:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        self.current_user = None

    def login(self, username, password):
        try:
            for u in self.user_repo():
                if u.username == username and u.password == password:
                    self.current_user = u
                    return True
            return False
        except Exception:
            return False

    def logout(self):
        self.current_user = None
