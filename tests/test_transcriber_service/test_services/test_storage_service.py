import unittest
from unittest.mock import MagicMock

from transcriber_service.interfaces.repositories_interfaces import IStorageRepository
from transcriber_service.services import StorageService


class TestStorageService(unittest.TestCase):
    def setUp(self):
        self.mock_storage_repository = MagicMock(spec=IStorageRepository)
        self.storage_service = StorageService(self.mock_storage_repository)

    def test_create_storage(self):
        storage = self.storage_service.create_storage('id')
        self.mock_storage_repository.add.assert_called_once_with(storage)

    def test_get_user_storage(self):
        self.mock_storage_repository.get_by_user.return_value = None
        self.assertEqual(self.storage_service.get_user_storage('id'), None)
        self.mock_storage_repository.get_by_user.assert_called_once_with('id')


if __name__ == '__main__':
    unittest.main()
