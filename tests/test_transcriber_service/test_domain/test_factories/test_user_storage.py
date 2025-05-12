import unittest

from transcriber_service.domain.entities.user import AuthUser, Admin
from transcriber_service.domain.factories import AuthUserFactory, AdminFactory
from transcriber_service.domain.interfaces import IUser


class TestAuthUserFactory(unittest.TestCase):
    def setUp(self):
        self.factory = AuthUserFactory()

    def test_create_user_returns_authuser(self):
        email = "user@example.com"
        password_hash = "hashed_password"

        user = self.factory.create_user(email, password_hash)

        self.assertIsInstance(user, IUser)
        self.assertIsInstance(user, AuthUser)

    def test_create_object_actual_implementation(self):
        user = self.factory.create_object()

        self.assertIsInstance(user, IUser)
        self.assertIsInstance(user, AuthUser)


class TestAdminFactory(unittest.TestCase):
    def setUp(self):
        self.factory = AdminFactory()

    def test_create_user_returns_admin(self):
        email = "admin@example.com"
        password_hash = "admin_hash"

        user = self.factory.create_user(email, password_hash)

        self.assertIsInstance(user, IUser)
        self.assertIsInstance(user, Admin)

    def test_create_object_actual_implementation(self):
        user = self.factory.create_object()

        self.assertIsInstance(user, IUser)
        self.assertIsInstance(user, Admin)


if __name__ == "__main__":
    unittest.main()
