from email_validator import validate_email
from password_strength import PasswordPolicy

from transcriber_service.application.serialization import UserDTO, UserMapper
from transcriber_service.domain.factories import (
    AuthUserFactory,
    AdminFactory,
    IUserFactory,
)
from transcriber_service.domain.interfaces import (
    IUserRepository,
    IUser,
    IPasswordManager,
)
from transcriber_service.application.services.istorage_service import IStorageService
import logging

logger = logging.getLogger(__name__)


class UserService(object):
    def __init__(
        self,
        repository: IUserRepository,
        storage_service: IStorageService,
        password_manager: IPasswordManager,
    ):
        self._repository = repository
        self._storage_service = storage_service
        self.password_hasher = password_manager
        self._user_factory: IUserFactory = AdminFactory()
        self._policy = PasswordPolicy.from_names(
            length=8, uppercase=1, numbers=1, special=1
        )
        self.mapper = UserMapper()

    def create_user(self, email: str, password: str) -> UserDTO:
        if self.get_user_by_email(email):
            logger.error(f"User with email {email} already exists")
            raise Exception("User already exists")

        errors = self._policy.test(password)
        if errors:
            logger.error(f"Error validating password: {errors}, {password}")
            raise Exception(
                f"Password is weak: 8 symbols, 1 uppercase, number, special"
            )

        email = validate_email(email).normalized
        password_hash = self.password_hasher.hash_password(password)
        self._user_factory = AuthUserFactory()
        user = self._user_factory.create_user(email, password_hash)

        self._repository.add(user)
        self._storage_service.create_storage(user.id)

        return self.mapper.to_dto(user)

    def create_admin(self, email: str, password: str) -> IUser:
        if self._repository.get_by_email(email):
            raise Exception("User already exists")
        if self._policy.test(password):
            raise Exception(
                f"Password is weak: 8 symbols, 1 uppercase, number, special"
            )

        email = validate_email(email).normalized
        password_hash = self.password_hasher.hash_password(password)
        self._user_factory = AdminFactory()
        user = self._user_factory.create_user(email, password_hash)

        self._repository.add(user)
        self._storage_service.create_storage(user.id)
        return user

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

    def get_user_by_email(self, email: str) -> IUser | None:
        return self._repository.get_by_email(email)

    def update_user(self, user: IUser):
        self._repository.update(user)

    def get_all(self) -> list[IUser]:
        return self._repository.get_all()
