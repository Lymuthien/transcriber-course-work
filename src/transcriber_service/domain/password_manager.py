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

        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    @staticmethod
    def create_password() -> str:
        """
        Create password from random 12 symbols.

        :return: Not hashed password."""

        password = secrets.token_urlsafe(12)
        return password

