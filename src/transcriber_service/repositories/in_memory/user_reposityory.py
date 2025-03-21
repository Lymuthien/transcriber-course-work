from ..interfaces.iuser_repository import IUserRepository
from ...domain.user import User


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._users: dict[str, User] = {}

    def get_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        return next((u for u in self._users.values() if u.email == email), None)

    def add(self, user: User) -> None:
        if user.id in self._users:
            raise ValueError("User already exists")
        self._users[user.id] = user

    def update(self, user: User) -> None:
        if user.id not in self._users:
            raise ValueError("User not found")
        self._users[user.id] = user

    def delete(self, user: User) -> None:
        if user.id not in self._users:
            raise ValueError("User not found")
        self._users.pop(user.id)