from src.models import User

class UserService:
    def __init__(self, repository):
        self.repository = repository

    def register_user(self, name, email, password):
        if not name or not email or not password:
            raise ValueError("All fields are required")

        if self.repository.find_by_email(email):
            raise ValueError("E-mail already registered")

        user = User(name, email, password)
        self.repository.save(user)
        return user

    def login(self, email, password):
        user = self.repository.find_by_email(email)
        if not user or user.password != password:
            raise ValueError("Invalid email or password")
        return user
