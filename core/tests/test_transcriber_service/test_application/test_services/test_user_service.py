import unittest
from unittest.mock import MagicMock, patch

from transcriber_service.application.services import IStorageService
from transcriber_service.domain.interfaces import (
    IUserRepository,
    IPasswordManager,
    IUser,
)
from transcriber_service.application.services.user_service import UserService


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.repository = MagicMock(spec=IUserRepository)
        self.storage_service = MagicMock(spec=IStorageService)
        self.password_manager = MagicMock(spec=IPasswordManager)
        self.password_policy = MagicMock()

        self.service = UserService(
            self.repository, self.storage_service, self.password_manager
        )
        self.service._policy = self.password_policy

        self.user = MagicMock(spec=IUser)
        self.user.id = "user_123"
        self.user.is_blocked = False

        self.admin = MagicMock(spec=IUser)
        self.admin.can_block.return_value = True

    @patch("transcriber_service.application.services.user_service.validate_email")
    def test_create_user_success(self, mock_validate_email):
        email = "user@example.com"
        password = "Password1!"
        normalized_email = "user@example.com"
        password_hash = "hashed_password"

        mock_validate_email.return_value.normalized = normalized_email
        self.password_policy.test.return_value = []
        self.password_manager.hash_password.return_value = password_hash
        self.repository.get_by_email.return_value = None
        user = MagicMock(spec=IUser)
        user.id = "user_123"
        with patch(
            "transcriber_service.application.services.user_service.AuthUserFactory"
        ) as mock_factory:
            mock_factory.return_value.create_user.return_value = user

            result = self.service.create_user(email, password)

            mock_validate_email.assert_called_once_with(email)
            self.password_policy.test.assert_called_once_with(password)
            self.password_manager.hash_password.assert_called_once_with(password)
            mock_factory.return_value.create_user.assert_called_once_with(
                normalized_email, password_hash
            )
            self.repository.add.assert_called_once_with(user)
            self.storage_service.create_storage.assert_called_once_with("user_123")
            self.assertEqual(result, user)

    @patch("transcriber_service.application.services.user_service.validate_email")
    def test_create_user_already_exists(self, mock_validate_email):
        email = "user@example.com"
        self.repository.get_by_email.return_value = self.user

        with self.assertRaises(Exception) as cm:
            self.service.create_user(email, "Password1!")

        self.repository.get_by_email.assert_called_once_with(email)
        mock_validate_email.assert_not_called()
        self.password_policy.test.assert_not_called()
        self.assertEqual(str(cm.exception), "User already exists")

    @patch("transcriber_service.application.services.user_service.validate_email")
    def test_create_user_weak_password(self, mock_validate_email):
        email = "user@example.com"
        self.repository.get_by_email.return_value = None
        self.password_policy.test.return_value = ["LengthError"]

        with self.assertRaises(Exception) as cm:
            self.service.create_user(email, "weak")

        self.repository.get_by_email.assert_called_once_with(email)
        mock_validate_email.assert_not_called()
        self.password_policy.test.assert_called_once_with("weak")
        self.assertEqual(str(cm.exception), "Password is weak")

    def test_block_user_success(self):
        target_email = "user@example.com"
        self.repository.get_by_email.return_value = self.user

        self.service.block_user(self.admin, target_email)

        self.admin.can_block.assert_called_once()
        self.repository.get_by_email.assert_called_once_with(target_email)
        self.assertTrue(self.user.is_blocked)
        self.repository.update.assert_called_once_with(self.user)

    def test_block_user_no_permission(self):
        initiator = MagicMock(spec=IUser)
        initiator.can_block.return_value = False

        with self.assertRaises(PermissionError) as cm:
            self.service.block_user(initiator, "user@example.com")

        initiator.can_block.assert_called_once()
        self.repository.get_by_email.assert_not_called()
        self.assertEqual(str(cm.exception), "Only admins can block users")

    def test_block_user_not_found(self):
        target_email = "user@example.com"
        self.repository.get_by_email.return_value = None

        with self.assertRaises(KeyError) as cm:
            self.service.block_user(self.admin, target_email)

        self.admin.can_block.assert_called_once()
        self.repository.get_by_email.assert_called_once_with(target_email)
        self.repository.update.assert_not_called()

    def test_unblock_user_success(self):
        target_email = "user@example.com"
        self.user.is_blocked = True
        self.repository.get_by_email.return_value = self.user

        self.service.unblock_user(self.admin, target_email)

        self.admin.can_block.assert_called_once()
        self.repository.get_by_email.assert_called_once_with(target_email)
        self.assertFalse(self.user.is_blocked)
        self.repository.update.assert_called_once_with(self.user)

    def test_unblock_user_no_permission(self):
        initiator = MagicMock(spec=IUser)
        initiator.can_block.return_value = False

        with self.assertRaises(PermissionError) as cm:
            self.service.unblock_user(initiator, "user@example.com")

        initiator.can_block.assert_called_once()
        self.repository.get_by_email.assert_not_called()
        self.assertEqual(str(cm.exception), "Only admins can unblock users")

    def test_unblock_user_not_found(self):
        target_email = "user@example.com"
        self.repository.get_by_email.return_value = None

        with self.assertRaises(KeyError) as cm:
            self.service.unblock_user(self.admin, target_email)

        self.admin.can_block.assert_called_once()
        self.repository.get_by_email.assert_called_once_with(target_email)
        self.repository.update.assert_not_called()

    def test_delete_user_success(self):
        target_email = "user@example.com"
        self.repository.get_by_email.return_value = self.user

        self.service.delete_user(self.admin, target_email)

        self.admin.can_block.assert_called_once()
        self.repository.get_by_email.assert_called_once_with(target_email)
        self.repository.delete.assert_called_once_with(self.user)

    def test_delete_user_no_permission(self):
        initiator = MagicMock(spec=IUser)
        initiator.can_block.return_value = False

        with self.assertRaises(PermissionError) as cm:
            self.service.delete_user(initiator, "user@example.com")

        initiator.can_block.assert_called_once()
        self.repository.get_by_email.assert_not_called()
        self.assertEqual(str(cm.exception), "Only admins can delete users")

    def test_delete_user_not_found(self):
        target_email = "user@example.com"
        self.repository.get_by_email.return_value = None

        with self.assertRaises(KeyError) as cm:
            self.service.delete_user(self.admin, target_email)

        self.admin.can_block.assert_called_once()
        self.repository.get_by_email.assert_called_once_with(target_email)
        self.repository.delete.assert_not_called()

    def test_get_user_by_email_found(self):
        email = "user@example.com"
        self.repository.get_by_email.return_value = self.user

        result = self.service.get_user_by_email(email)

        self.repository.get_by_email.assert_called_once_with(email)
        self.assertEqual(result, self.user)

    def test_get_user_by_email_not_found(self):
        email = "user@example.com"
        self.repository.get_by_email.return_value = None

        result = self.service.get_user_by_email(email)

        self.repository.get_by_email.assert_called_once_with(email)
        self.assertIsNone(result)

    def test_update_user(self):
        self.service.update_user(self.user)

        self.repository.update.assert_called_once_with(self.user)


if __name__ == "__main__":
    unittest.main()
