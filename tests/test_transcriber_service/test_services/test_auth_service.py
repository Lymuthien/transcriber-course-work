import unittest
from unittest.mock import MagicMock

from transcriber_service.interfaces.iuser import IUser
from transcriber_service.domain import AuthException, Admin
from transcriber_service.interfaces.iuser_repository import IUserRepository
from transcriber_service.services import StorageService, AuthService


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.mock_user_repository = MagicMock(spec=IUserRepository)
        self.mock_storage_service = MagicMock(spec=StorageService)

        self.auth_service = AuthService(self.mock_user_repository, self.mock_storage_service)

    def test_register_user(self):
        self.mock_user_repository.get_by_email.return_value = None
        self.auth_service.register_user('email@mail.ru', 'coRR126**e')

        self.mock_user_repository.add.assert_called_once()
        self.mock_storage_service.create_storage.assert_called_once()

    def test_register_user_already_exists_raises_error(self):
        self.mock_user_repository.get_by_email.return_value = ''
        with self.assertRaises(AuthException):
            self.auth_service.register_user(email='<EMAIL>', password='<PASSWORD>')

    def test_register_user_weak_password_raises_error(self):
        self.mock_user_repository.get_by_email.return_value = None
        with self.assertRaises(AuthException):
            self.auth_service.register_user(email='<EMAIL>', password='<PASSWORD>')

    def test_block_user(self):
        mock_admin = MagicMock(spec=Admin)
        mock_user = MagicMock(spec=IUser)
        self.mock_user_repository.get_by_email.return_value = mock_user

        self.auth_service.block_user(mock_admin, '<EMAIL>')
        self.mock_user_repository.get_by_email.assert_called_once_with('<EMAIL>')

    def test_block_user_initiator_not_admin_raises_error(self):
        mock_user = MagicMock(spec=IUser)
        with self.assertRaises(PermissionError):
            self.auth_service.block_user(mock_user, '<EMAIL>')

    def test_block_user_not_found_raises_error(self):
        mock_admin = MagicMock(spec=Admin)
        self.mock_user_repository.get_by_email.return_value = None

        with self.assertRaises(AuthException):
            self.auth_service.block_user(mock_admin, '<EMAIL>')

    def test_unblock_user(self):
        mock_admin = MagicMock(spec=Admin)
        mock_user = MagicMock(spec=IUser)
        self.mock_user_repository.get_by_email.return_value = mock_user

        self.auth_service.unblock_user(mock_admin, '<EMAIL>')
        self.mock_user_repository.get_by_email.assert_called_once_with('<EMAIL>')

    def test_unblock_user_initiator_not_admin_raises_error(self):
        mock_user = MagicMock(spec=IUser)
        with self.assertRaises(PermissionError):
            self.auth_service.unblock_user(mock_user, '<EMAIL>')

    def test_unblock_user_not_found_raises_error(self):
        mock_admin = MagicMock(spec=Admin)
        self.mock_user_repository.get_by_email.return_value = None

        with self.assertRaises(AuthException):
            self.auth_service.unblock_user(mock_admin, '<EMAIL>')

    def test_delete_user(self):
        mock_admin = MagicMock(spec=Admin)
        mock_user = MagicMock(spec=IUser)
        self.mock_user_repository.get_by_email.return_value = mock_user

        self.auth_service.delete_user(mock_admin, '<EMAIL>')
        self.mock_user_repository.get_by_email.assert_called_once_with('<EMAIL>')
        self.mock_user_repository.delete.assert_called_once_with(mock_user)

    def test_delete_user_initiator_not_admin_raises_error(self):
        mock_user = MagicMock(spec=IUser)
        with self.assertRaises(PermissionError):
            self.auth_service.delete_user(mock_user, '<EMAIL>')

    def test_delete_user_not_found_raises_error(self):
        mock_admin = MagicMock(spec=Admin)
        self.mock_user_repository.get_by_email.return_value = None

        with self.assertRaises(AuthException):
            self.auth_service.delete_user(mock_admin, '<EMAIL>')

    def test_create_admin(self):
        self.mock_user_repository.get_by_email.return_value = None
        self.auth_service.create_admin('email@mail.ru', 'coRR126**e')

        self.mock_user_repository.add.assert_called_once()
        self.mock_storage_service.create_storage.assert_called_once()

    def test_create_admin_already_exists_raises_error(self):
        self.mock_user_repository.get_by_email.return_value = ''
        with self.assertRaises(AuthException):
            self.auth_service.create_admin(email='<EMAIL>', password='<PASSWORD>')

    def test_create_admin_weak_password_raises_error(self):
        self.mock_user_repository.get_by_email.return_value = None
        with self.assertRaises(AuthException):
            self.auth_service.create_admin(email='<EMAIL>', password='<PASSWORD>')

    def test_change_password(self):
        mock_user = MagicMock(spec=IUser)
        self.mock_user_repository.get_by_email.return_value = mock_user

        self.auth_service.change_password('<EMAIL>', 'pass', ';ldf;lSDL54-*')

        mock_user.change_password.assert_called_once_with('pass', ';ldf;lSDL54-*')
        self.mock_user_repository.update.assert_called_once_with(mock_user)

    def test_change_password_user_not_found_raises_error(self):
        self.mock_user_repository.get_by_email.return_value = None
        with self.assertRaises(AuthException):
            self.auth_service.change_password('<EMAIL>', 'pass', ';ldf;lSDL54-*')

    def test_recover_password_user_not_found_raises_error(self):
        self.mock_user_repository.get_by_email.return_value = None
        with self.assertRaises(AuthException):
            self.auth_service.recover_password('<EMAIL>')


if __name__ == '__main__':
    unittest.main()
