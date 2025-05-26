import pytest
from src.repository import UserRepository
from src.service import UserService

@pytest.fixture
def service():
    return UserService(UserRepository())

def test_register_valid_user(service):
    user = service.register_user("Ana", "ana@email.com", "123")
    assert user.email == "ana@email.com"

def test_register_user_with_existing_email(service):
    service.register_user("Ana", "ana@email.com", "123")
    with pytest.raises(ValueError, match="E-mail already registered"):
        service.register_user("Ana2", "ana@email.com", "456")

def test_register_user_with_missing_fields(service):
    with pytest.raises(ValueError, match="All fields are required"):
        service.register_user("", "ana@email.com", "123")

def test_login_success(service):
    service.register_user("Ana", "ana@email.com", "123")
    user = service.login("ana@email.com", "123")
    assert user.name == "Ana"

def test_login_invalid_password(service):
    service.register_user("Ana", "ana@email.com", "123")
    with pytest.raises(ValueError, match="Invalid email or password"):
        service.login("ana@email.com", "wrong")

def test_login_nonexistent_email(service):
    with pytest.raises(ValueError, match="Invalid email or password"):
        service.login("nao@existe.com", "123")
