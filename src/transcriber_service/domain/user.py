from uuid import uuid4
import hashlib
from email_validator import validate_email
from .exceptions import InvalidEmailException


class User(object):
    def __init__(self, email: str, password: str):
        self.__email = self.__validated_normalized_email(email)
        self.__id = uuid4()
        self.__password_hash = self.__hash_password(password)
        self._role = "guest"

    @staticmethod
    def __hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def __validated_normalized_email(email: str) -> str:
        try:
            return validate_email(email).normalized
        except Exception as e:
            raise InvalidEmailException(str(e))

    @property
    def id(self) -> str:
        return str(self.__id)

    @property
    def email(self) -> str:
        return self.__email

    @property
    def role(self) -> str:
        return self._role

    def verify_password(self, password: str) -> bool:
        return self.__password_hash == self.__hash_password(password)

    def change_password(self, current_password: str, new_password: str) -> bool:
        if self.verify_password(current_password):
            self.__password_hash = self.__hash_password(new_password)
            return True
        else:
            return False


class AuthUser(User):
    def __init__(self, email: str, password: str):
        super().__init__(email, password)
        self._role = "user"


class Admin(AuthUser):
    def __init__(self, email: str, password: str):
        super().__init__(email, password)
        self._role = "admin"
