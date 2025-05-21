from password_strength import PasswordPolicy

from transcriber_service.application.serialization import UserDTO, UserMapper
from transcriber_service.domain.factories import (
    IUserFactory,
)
from transcriber_service.domain.interfaces import (
    IUserRepository,
    IUser,
)
from transcriber_service.application.services.istorage_service import IStorageService
import logging

logger = logging.getLogger(__name__)


class UserService(object):
    def __init__(
        self,
        repository: IUserRepository,
        storage_service: IStorageService,
    ):
        self._repository = repository
        self._storage_service = storage_service
        self._user_factory: IUserFactory | None = None
        self._policy = PasswordPolicy.from_names(
            length=8, uppercase=1, numbers=1, special=1
        )
        self.mapper = UserMapper()

    def create_user(self, email: str, password: str, factory: IUserFactory) -> UserDTO:
        self._user_factory = factory
        user = self._user_factory.create_user(email, password)

        self._repository.add(user)
        self._storage_service.create_storage(user.id)

        return self.mapper.to_dto(user)

    def block_user(self, initiator: IUser, target_email: str):
        if not initiator.can_block():
            raise PermissionError("Only admins can block users")

        user = self._repository.get_by_email(target_email)
        if not user:
            raise KeyError("User not found")

        user.is_blocked = True
        self._repository.update(user)

    def unblock_user(self, initiator: IUser, target_email: str):
        if not initiator.can_block():
            raise PermissionError("Only admins can unblock users")

        user = self._repository.get_by_email(target_email)
        if not user:
            raise KeyError("User not found")

        user.is_blocked = False
        self._repository.update(user)

    def delete_user(self, initiator: IUser, target_email: str):
        if not initiator.can_block():
            raise PermissionError("Only admins can delete users")

        user = self._repository.get_by_email(target_email)
        if not user:
            raise KeyError("User not found")

        self._repository.delete(user)

    def get_user_by_email(self, email: str) -> UserDTO | None:
        user = self._repository.get_by_email(email)
        return self.mapper.to_dto(user)

    def update_user(self, user: IUser):
        self._repository.update(user)

    def get_all(self) -> list[UserDTO]:
        users = self._repository.get_all()
        return [self.mapper.to_dto(user) for user in users]
