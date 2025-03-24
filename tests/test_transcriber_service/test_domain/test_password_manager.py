import unittest

from transcriber_service.domain.password_manager import PasswordManager


class TestPasswordManager(unittest.TestCase):
    def test_hash_password_doesnt_match_original_password(self):
        password = 'lala8687987SDF;J'
        self.assertNotEqual(password, PasswordManager.hash_password(password))

    def test_hash_one_password_always_returns_one_value(self):
        password = 'lala8687987SDF;J'
        self.assertEqual(PasswordManager.hash_password(password), PasswordManager.hash_password(password))

    def test_create_password_returns_different_passwords(self):
        self.assertNotEqual(PasswordManager.create_password(), PasswordManager.create_password())

if __name__ == '__main__':
    unittest.main()
