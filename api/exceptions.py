class UserNotFoundException(Exception):
    def __init__(self, login: str):
        self.login = login
        self.message = f"User not found"
        super().__init__(self.message)

    def to_dict(self):
        return {"error": self.message, "invalid_login": self.login}
