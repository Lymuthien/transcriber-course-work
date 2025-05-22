import unittest
from datetime import datetime

from transcriber_service.domain import User, AuthException


class TestUser(unittest.TestCase):
    def setUp(self):
        self.email = "tanya@mail.ru"
        self.password = "<PASSWORD>"
        self.user = User(self.email, self.password)

    def test_is_blocked_basically_returns_false(self):
        self.assertEqual(self.user.is_blocked, False)

    def test_is_blocked_setter(self):
        self.user.is_blocked = True
        self.assertEqual(self.user.is_blocked, True)
        self.user.is_blocked = False

    def test_id_returns_string(self):
        self.assertEqual(type(self.user.id), str)

    def test_email_returns_correct(self):
        self.assertEqual(self.user.email, self.email)

    def test_registration_date_returns_datetime(self):
        self.assertEqual(type(self.user.registration_date), datetime)

    def test_last_updated_returns_datetime(self):
        self.assertEqual(type(self.user.last_updated), datetime)


if __name__ == "__main__":
    unittest.main()
