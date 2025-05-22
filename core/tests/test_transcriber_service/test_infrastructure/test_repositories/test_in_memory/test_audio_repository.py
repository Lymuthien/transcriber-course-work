import unittest
from unittest.mock import MagicMock

from transcriber_service.domain.interfaces import (
    IStorageRepository,
    IAudioRecord,
    IStorage,
    IFileManager,
    ISerializer,
)
from transcriber_service.infrastructure.repositories import LocalAudioRepository


class TestLocalAudioRepository(unittest.TestCase):
    def setUp(self):
        self.mock_saver = MagicMock(spec=IFileManager)
        self.mock_serializer = MagicMock(spec=ISerializer)
        self.mock_saver.save = MagicMock()
        self.mock_saver.load = {}

        self.mock_storage_repo = MagicMock(spec=IStorageRepository)
        self.mock_storage_repo.get_by_id.return_value = MagicMock(spec=IStorage)

        self.data_dir = " "
        self.local_audio_repository = LocalAudioRepository(
            self.mock_storage_repo, self.data_dir, self.mock_saver, self.mock_serializer
        )

    def test_add(self):
        mock_audio = MagicMock(spec=IAudioRecord)
        mock_audio.id.return_value = "1"
        self.local_audio_repository.add(mock_audio)

    def test_add_twice_raises_error(self):
        mock_audio = MagicMock(spec=IAudioRecord)
        mock_audio.id.return_value = "2"
        self.local_audio_repository.add(mock_audio)
        with self.assertRaises(ValueError):
            self.local_audio_repository.add(mock_audio)

    def test_get_by_id(self):
        mock_audio = MagicMock(spec=IAudioRecord)
        mock_audio.id.return_value = "3"
        self.local_audio_repository.add(mock_audio)

        self.assertEqual(
            self.local_audio_repository.get_by_id(mock_audio.id), mock_audio
        )

    def test_delete(self):
        mock_audio = MagicMock(spec=IAudioRecord)
        mock_audio.id.return_value = "4"
        self.local_audio_repository.add(mock_audio)
        self.local_audio_repository.delete(mock_audio.id)
        self.assertEqual(self.local_audio_repository.get_by_id(mock_audio.id), None)

    def test_delete_not_found_raises_error(self):
        with self.assertRaises(ValueError):
            self.local_audio_repository.delete("None")

    def test_update_not_found_raises_error(self):
        mock_audio = MagicMock(spec=IAudioRecord)
        mock_audio.id.return_value = "5"
        with self.assertRaises(ValueError):
            self.local_audio_repository.update(mock_audio)


if __name__ == "__main__":
    unittest.main()
