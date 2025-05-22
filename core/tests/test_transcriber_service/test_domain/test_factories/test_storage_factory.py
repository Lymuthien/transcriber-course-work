import unittest
from unittest.mock import MagicMock, patch

from transcriber_service.domain.entities.storage import Storage
from transcriber_service.domain.factories import StorageFactory
from transcriber_service.domain.interfaces import IStorage


class TestStorageFactory(unittest.TestCase):
    def setUp(self):
        self.factory = StorageFactory()

    @patch("transcriber_service.domain.entities.storage.Storage")
    def test_create_storage_returns_storage_with_user_id(self, mock_storage):
        test_user_id = "test_user_123"

        result = self.factory.create_storage(test_user_id)

        self.assertIsInstance(result, IStorage)

    def test_create_storage_with_actual_implementation(self):
        test_user_id = "test_user_123"

        result = self.factory.create_storage(test_user_id)

        self.assertIsInstance(result, IStorage)


if __name__ == "__main__":
    unittest.main()
