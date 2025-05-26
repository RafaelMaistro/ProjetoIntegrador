class UserRepository:
    def __init__(self):
        self.users = {}

    def save(self, user):
        if user.email in self.users:
            raise ValueError("E-mail already exists")
        self.users[user.email] = user

    def find_by_email(self, email):
        return self.users.get(email)
