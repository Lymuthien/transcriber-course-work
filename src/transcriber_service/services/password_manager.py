import hashlib
import secrets


class PasswordManager(object):
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    @staticmethod
    def create_password():
        password = secrets.token_urlsafe(12)
        return password

