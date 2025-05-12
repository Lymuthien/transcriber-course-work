import unittest
import hashlib

from transcriber_service.infrastructure.services import PasswordManager


class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        self.manager = PasswordManager()

    def test_hash_password(self):
        password = "MyPassword123!"
        result = self.manager.hash_password(password)

        self.assertIsInstance(result, str)
        expected = hashlib.sha512(password.encode("utf-8")).hexdigest()
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 128)

    def test_hash_password_empty(self):
        password = ""
        result = self.manager.hash_password(password)

        self.assertIsInstance(result, str)
        expected = hashlib.sha512("".encode("utf-8")).hexdigest()
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 128)

    def test_create_password(self):
        result = self.manager.create_password()

        self.assertIsInstance(result, str)
        self.assertGreaterEqual(len(result), 12)
        self.assertTrue(
            all(
                c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
                for c in result
            )
        )

    def test_create_password_unique(self):
        password1 = self.manager.create_password()
        password2 = self.manager.create_password()

        self.assertNotEqual(password1, password2)

    def test_verify_password_correct(self):
        password = "MyPassword123!"
        hashed = self.manager.hash_password(password)
        result = self.manager.verify_password(hashed, password)

        self.assertTrue(result)

    def test_verify_password_incorrect(self):
        password = "MyPassword123!"
        wrong_password = "WrongPassword!"
        hashed = self.manager.hash_password(password)
        result = self.manager.verify_password(hashed, wrong_password)

        self.assertFalse(result)

    def test_verify_password_empty(self):
        password = ""
        hashed = self.manager.hash_password(password)
        result = self.manager.verify_password(hashed, "")

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
