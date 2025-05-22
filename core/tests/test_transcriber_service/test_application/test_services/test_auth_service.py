import unittest
from unittest.mock import MagicMock
from transcriber_service.application.services.user_service import UserService
from transcriber_service.domain.interfaces import IUser, IEmailService, IPasswordManager
from transcriber_service.domain import AuthException
from transcriber_service.application.services.auth_service import AuthService
from transcriber_service.infrastructure import PasswordManager


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.user_service = MagicMock(spec=UserService)
        self.password_hasher = MagicMock()
        self.user_service.password_hasher = self.password_hasher
        self.email_service = MagicMock(spec=IEmailService)
        self.password_manager = MagicMock(spec=IPasswordManager)

        self.password_policy = MagicMock()

        self.service = AuthService(
            self.user_service,
            self.email_service,
            self.password_manager,
        )
        self.service._AuthService__email_service = self.email_service
        self.service._AuthService__policy = self.password_policy

        self.user = MagicMock(spec=IUser)
        self.user.email = "user@example.com"
        self.user.password_hash = "hashed_password"
        self.user.temp_password_hash = None
        self.user.is_blocked = False

    def test_register_user_success(self):
        self.user_service.create_user.return_value = self.user

        result = self.service.register_user("user@example.com", "Password1!")

        self.user_service.create_user.assert_called_once_with(
            "user@example.com", "Password1!"
        )
        self.assertEqual(result, self.user)

    def test_create_admin_success(self):
        admin = MagicMock(spec=IUser)
        self.user_service.create_admin.return_value = admin

        result = self.service.create_admin("admin@example.com", "Admin1!")

        self.user_service.create_admin.assert_called_once_with(
            "admin@example.com", "Admin1!"
        )
        self.assertEqual(result, admin)

    def test_login_success(self):
        self.user_service.get_user_by_email.return_value = self.user
        self.password_hasher.verify_password.return_value = True

        result = self.service.login("user@example.com", "Password1!")

        self.user_service.get_user_by_email.assert_called_once_with("user@example.com")
        self.password_hasher.verify_password.assert_called_once_with(
            "hashed_password", "Password1!"
        )
        self.assertEqual(result, self.user)

    def test_login_invalid_credentials(self):
        self.user_service.get_user_by_email.return_value = None

        with self.assertRaises(AuthException) as cm:
            self.service.login("user@example.com", "Password1!")

        self.user_service.get_user_by_email.assert_called_once_with("user@example.com")
        self.password_hasher.verify_password.assert_not_called()
        self.assertEqual(str(cm.exception), "Invalid credentials")

    def test_login_wrong_password(self):
        self.user_service.get_user_by_email.return_value = self.user
        self.password_hasher.verify_password.return_value = False

        with self.assertRaises(AuthException) as cm:
            self.service.login("user@example.com", "WrongPassword!")

        self.user_service.get_user_by_email.assert_called_once_with("user@example.com")
        self.password_hasher.verify_password.assert_called_once_with(
            "hashed_password", "WrongPassword!"
        )
        self.assertEqual(str(cm.exception), "Invalid credentials")

    def test_login_blocked_user(self):
        self.user.is_blocked = True
        self.user_service.get_user_by_email.return_value = self.user
        self.password_hasher.verify_password.return_value = True

        with self.assertRaises(AuthException) as cm:
            self.service.login("user@example.com", "Password1!")

        self.user_service.get_user_by_email.assert_called_once_with("user@example.com")
        self.password_hasher.verify_password.assert_called_once_with(
            "hashed_password", "Password1!"
        )
        self.assertEqual(str(cm.exception), "User is blocked")

    def test_change_password_success(self):
        self.user_service.get_user_by_email.return_value = self.user
        self.password_hasher.verify_password.return_value = True
        self.password_policy.test.return_value = []

        self.service.change_password("user@example.com", "Password1!", "NewPassword1!")

        self.user_service.get_user_by_email.assert_called_once_with("user@example.com")
        self.password_hasher.verify_password.assert_called_once_with(
            "hashed_password", "Password1!"
        )
        self.password_policy.test.assert_called_once_with("NewPassword1!")
        self.assertEqual(self.user.password_hash, "NewPassword1!")
        self.user_service.update_user.assert_called_once_with(self.user)

    def test_change_password_user_not_found(self):
        self.user_service.get_user_by_email.return_value = None

        with self.assertRaises(AuthException) as cm:
            self.service.change_password(
                "user@example.com", "Password1!", "NewPassword1!"
            )

        self.user_service.get_user_by_email.assert_called_once_with("user@example.com")
        self.password_hasher.verify_password.assert_not_called()
        self.password_policy.test.assert_not_called()
        self.assertEqual(str(cm.exception), "User not found")

    def test_change_password_incorrect_current_password(self):
        self.user_service.get_user_by_email.return_value = self.user
        self.password_hasher.verify_password.return_value = False
        self.password_policy.test.return_value = None

        with self.assertRaises(AuthException) as cm:
            self.service.change_password(
                "user@example.com", "WrongPassword!", "NewPassword1!"
            )

        self.user_service.get_user_by_email.assert_called_once_with("user@example.com")
        self.password_hasher.verify_password.assert_called_once_with(
            "hashed_password", "WrongPassword!"
        )
        self.assertEqual(str(cm.exception), "Incorrect password")

    def test_change_password_weak_password(self):
        self.user_service.get_user_by_email.return_value = self.user
        self.password_hasher.verify_password.return_value = True
        self.password_policy.test.return_value = ["LengthError", "UppercaseError"]

        with self.assertRaises(AuthException) as cm:
            self.service.change_password("user@example.com", "Password1!", "weak")

        self.user_service.get_user_by_email.assert_called_once_with("user@example.com")
        self.password_policy.test.assert_called_once_with("weak")
        self.assertEqual(
            str(cm.exception), "Password is weak: ['LengthError', 'UppercaseError']"
        )
        self.user_service.update_user.assert_not_called()

    def test_recover_password_success(self):
        self.user_service.get_user_by_email.return_value = self.user
        self.password_hasher.create_password.return_value = "TempPass1!"
        self.password_hasher.hash_password.return_value = "hashed_temp_pass"

        self.service.recover_password("user@example.com")

        self.user_service.get_user_by_email.assert_called_once_with("user@example.com")
        self.password_hasher.create_password.assert_called_once()
        self.password_hasher.hash_password.assert_called_once_with("TempPass1!")
        self.assertEqual(self.user.temp_password_hash, "hashed_temp_pass")
        self.email_service.send_recovery_email.assert_called_once_with(
            "user@example.com", "TempPass1!"
        )
        self.user_service.update_user.assert_called_once_with(self.user)

    def test_recover_password_user_not_found(self):
        self.user_service.get_user_by_email.return_value = None

        with self.assertRaises(AuthException) as cm:
            self.service.recover_password("user@example.com")

        self.user_service.get_user_by_email.assert_called_once_with("user@example.com")
        self.password_hasher.create_password.assert_not_called()
        self.email_service.send_recovery_email.assert_not_called()
        self.assertEqual(str(cm.exception), "User not found")


if __name__ == "__main__":
    unittest.main()
