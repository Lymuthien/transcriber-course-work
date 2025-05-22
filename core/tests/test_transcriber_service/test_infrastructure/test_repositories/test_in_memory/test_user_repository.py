import unittest
from unittest.mock import MagicMock

from transcriber_service.domain.interfaces import IUser, IFileManager, ISerializer
from transcriber_service.infrastructure.repositories.in_memory.user_reposityory import (
    LocalUserRepository,
)


class TestLocalUserRepository(unittest.TestCase):
    def setUp(self):
        self.mock_saver = MagicMock(spec=IFileManager)
        self.mock_serializer = MagicMock(spec=ISerializer)
        self.mock_saver.save = MagicMock()
        self.mock_saver.load = {}

        self.data_dir = " "
        self.local_user_repository = LocalUserRepository(
            self.data_dir, self.mock_saver, self.mock_serializer
        )

    def test_add(self):
        mock_user = MagicMock(spec=IUser)
        mock_user.id.return_value = "1"
        self.local_user_repository.add(mock_user)

    def test_add_twice_raises_error(self):
        mock_user = MagicMock(spec=IUser)
        mock_user.id.return_value = "1"
        self.local_user_repository.add(mock_user)
        with self.assertRaises(ValueError):
            self.local_user_repository.add(mock_user)

    def test_get_by_id(self):
        mock_user = MagicMock(spec=IUser)
        mock_user.id.return_value = "1"
        self.local_user_repository.add(mock_user)

        self.assertEqual(self.local_user_repository.get_by_id(mock_user.id), mock_user)

    def test_get_by_id_not_found_returns_none(self):
        self.assertEqual(self.local_user_repository.get_by_id("4"), None)

    def test_get_by_email(self):
        mock_user = MagicMock(spec=IUser)
        mock_user.id.return_value = "1"
        mock_user.email.return_value = "<EMAIL>"
        self.local_user_repository.add(mock_user)

        self.assertEqual(
            self.local_user_repository.get_by_email(mock_user.email), mock_user
        )

    def test_get_by_email_not_found_returns_none(self):
        self.assertEqual(self.local_user_repository.get_by_email("4"), None)

    def test_update_not_found_raises_error(self):
        mock_user = MagicMock(spec=IUser)
        mock_user.id.return_value = "1"
        with self.assertRaises(ValueError):
            self.local_user_repository.update(mock_user)

    def test_delete(self):
        mock_user = MagicMock(spec=IUser)
        mock_user.id.return_value = "1"
        self.local_user_repository.add(mock_user)
        self.local_user_repository.delete(mock_user)
        self.assertEqual(self.local_user_repository.get_by_id(mock_user.id), None)

    def test_delete_not_found_raises_error(self):
        mock_user = MagicMock(spec=IUser)
        mock_user.id.return_value = "1"
        with self.assertRaises(ValueError):
            self.local_user_repository.delete(mock_user)


if __name__ == "__main__":
    unittest.main()
