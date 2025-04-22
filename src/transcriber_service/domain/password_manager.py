import hashlib
import secrets


class PasswordManager(object):
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password.

        :param password: Password to hash.
        :return: Hash result.
        """

        return hashlib.sha512(password.encode("utf-8")).hexdigest()

    @staticmethod
    def create_password() -> str:
        """
        Create password.

        :return: Not hashed password."""

        password = secrets.token_urlsafe(12)
        return password

    @staticmethod
    def verify_password(hashed_password: str, other: str) -> bool:
        return hashed_password == PasswordManager.hash_password(other)
