import unittest
from datetime import datetime

from transcriber_service.domain import User, AuthException


class TestUser(unittest.TestCase):
    def setUp(self):
        self.email = 'tanya@mail.ru'
        self.password = '<PASSWORD>'
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

    def test_verify_password_returns_true_with_correct_password(self):
        self.assertTrue(self.user.verify_password(self.password))

    def test_verify_password_returns_false_with_incorrect_password(self):
        self.assertFalse(self.user.verify_password('incorrect'))

    def test_change_password_raise_error_with_incorrect_password(self):
        with self.assertRaises(AuthException):
            self.user.change_password('self.password', 'blabla')

    def test_change_password(self):
        self.user.change_password(self.password, 'new password')
        self.password = 'new password'
        self.assertTrue(self.user.verify_password(self.password))

    def test_generate_temp_password_returns_string(self):
        self.assertEqual(type(self.user.generate_temp_password()), str)

    def test_generate_password_can_auth(self):
        temp = self.user.generate_temp_password()
        self.assertTrue(self.user.verify_password(temp))
        self.password = temp

    def test_temp_password_change_general_password_after_auth(self):
        temp = self.user.generate_temp_password()
        self.user.verify_password(temp)
        self.assertFalse(self.user.verify_password(self.password))


if __name__ == '__main__':
    unittest.main()
