import unittest
from unittest.mock import MagicMock

from transcriber_service.interfaces.ifile_manager import IFileManager
from transcriber_service.interfaces.domain_interfaces import IStorage
from transcriber_service.repositories.in_memory.storage_repository import LocalStorageRepository


class TestLocalStorageRepository(unittest.TestCase):
    def setUp(self):
        self.mock_saver = MagicMock(spec=IFileManager)
        self.mock_saver.save = MagicMock()
        self.mock_saver.load = {}, {}

        self.data_dir = ' '
        self.local_storage_repository = LocalStorageRepository(self.data_dir, self.mock_saver)

    def test_add(self):
        mock_storage = MagicMock(spec=IStorage)
        mock_storage.id.return_value = '1'
        mock_storage.user_id.return_value = '1'
        self.local_storage_repository.add(mock_storage)

    def test_add_twice_raises_error(self):
        mock_storage = MagicMock(spec=IStorage)
        mock_storage.id.return_value = '2'
        mock_storage.user_id.return_value = '2'
        self.local_storage_repository.add(mock_storage)
        with self.assertRaises(ValueError):
            self.local_storage_repository.add(mock_storage)

    def test_get_by_id(self):
        mock_storage = MagicMock(spec=IStorage)
        mock_storage.id.return_value = '1'
        mock_storage.user_id.return_value = '1'
        self.local_storage_repository.add(mock_storage)

        self.assertEqual(self.local_storage_repository.get_by_id(mock_storage.id), mock_storage)

    def test_get_by_id_not_found_returns_none(self):
        self.assertEqual(self.local_storage_repository.get_by_id('4'), None)

    def test_get_by_user(self):
        mock_storage = MagicMock(spec=IStorage)
        mock_storage.id.return_value = '1'
        mock_storage.user_id.return_value = '1'
        self.local_storage_repository.add(mock_storage)

        self.assertEqual(self.local_storage_repository.get_by_user(mock_storage.user_id), mock_storage)

    def test_get_by_user_not_found_returns_none(self):
        self.assertEqual(self.local_storage_repository.get_by_user('4'), None)

    def test_update_not_found_raises_error(self):
        mock_storage = MagicMock(spec=IStorage)
        mock_storage.id.return_value = '1'
        with self.assertRaises(ValueError):
            self.local_storage_repository.update(mock_storage)

    def test_get_all_records(self):
        mock_storage = MagicMock(spec=IStorage)
        mock_storage.id.return_value = '1'
        mock_storage.user_id.return_value = '1'
        mock_storage.audio_record_ids.return_value = ['1', '2']
        self.local_storage_repository.add(mock_storage)

        self.assertEqual(self.local_storage_repository.get_all_records(mock_storage.id), mock_storage.audio_record_ids)

    def test_get_all_records_not_found_returns_empty_list(self):
        self.assertEqual(self.local_storage_repository.get_all_records('4'), [])


if __name__ == '__main__':
    unittest.main()
