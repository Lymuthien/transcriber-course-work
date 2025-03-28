from os.path import exists

from .local_file_manager import LocalPickleFileManager
from ...interfaces.ifile_manager import IFileManager
from ...interfaces.iuser_repository import IUserRepository
from ...domain import User


class LocalUserRepository(IUserRepository):
    def __init__(self, data_dir: str, file_manager: IFileManager = LocalPickleFileManager):
        """
        Create local user repository.

        :param data_dir: Directory to store local user data.
        """

        self.__file_manager = file_manager
        self._users: dict[str, User] = {}
        self.__dir: str = data_dir

        try:
            self._users = self.__file_manager.load(data_dir)
        except:
            pass

    def get_by_id(self, user_id: str) -> User | None:
        """Return user by its ID if it exists else None."""

        return self._users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        """Return user by email if it exists else None."""

        return next((u for u in self._users.values() if u.email == email), None)

    def add(self, user: User) -> None:
        """
        Add user to repository.

        :param user: New user.
        :raise ValueError: If user already exists.
        """

        if user.id in self._users:
            raise ValueError("User already exists")
        self._users[user.id] = user
        self.__file_manager.save(self._users, self.__dir)

    def update(self, user: User) -> None:
        """
        Update user in repository.

        :param user: New user value.
        :raise ValueError: If user does not exist.
        """

        if user.id not in self._users:
            raise ValueError("User not found")
        self._users[user.id] = user
        self.__file_manager.save(self._users, self.__dir)

    def delete(self, user: User) -> None:
        """
        Delete user from repository.

        :param user: Target user.
        :raise ValueError: If user does not exist.
        """

        if user.id not in self._users:
            raise ValueError("User not found")
        self._users.pop(user.id)
        self.__file_manager.save(self._users, self.__dir)
