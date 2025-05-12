import unittest
from unittest.mock import MagicMock

from transcriber_service.domain.factories import AudioRecordFactory
from transcriber_service.domain.interfaces import IAudioRecord


class TestAudioRecordFactory(unittest.TestCase):
    def setUp(self):
        self.factory = AudioRecordFactory()
        self.mock_audio_record = MagicMock(spec=IAudioRecord)

    def test_create_audio_returns_audio_record(self):
        test_data = {
            "file_name": "test.mp3",
            "file_path": "/path/to/test.mp3",
            "storage_id": "12345",
            "text": "test text",
            "language": "en",
        }

        result = self.factory.create_audio(**test_data)

        self.assertIsInstance(result, IAudioRecord)

    def test_create_object_returns_empty_audio_record(self):
        result = self.factory.create_object()

        self.assertIsInstance(result, IAudioRecord)
        self.assertEqual(result.file_path, "")
        self.assertEqual(result.storage_id, "")
        self.assertEqual(result.text, "")
        self.assertEqual(result.language, "")


if __name__ == "__main__":
    unittest.main()
