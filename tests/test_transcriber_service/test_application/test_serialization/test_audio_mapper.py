import unittest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from transcriber_service.application.serialization import (
    AudioRecordMapper,
    AudioRecordDTO,
)
from transcriber_service.domain.factories import IAudioRecordFactory
from transcriber_service.domain.interfaces import IAudioRecord


class TestAudioRecordMapper(unittest.TestCase):
    def setUp(self):
        self.mock_factory = MagicMock(spec=IAudioRecordFactory)
        self.mapper = AudioRecordMapper(factory=self.mock_factory)

        self.mock_audio = MagicMock(spec=IAudioRecord)
        self.mock_audio.id = "audio123"
        self.mock_audio.record_name = "test_recording"
        self.mock_audio.file_path = "/path/to/audio"
        self.mock_audio.storage_id = "storage123"
        self.mock_audio.text = "test text"
        self.mock_audio.language = "en"
        self.mock_audio.tags = ["music", "podcast"]
        self.mock_audio.last_updated = datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )

        self.test_dto = AudioRecordDTO(
            entity_type="audio_record",
            id="audio123",
            record_name="test_recording",
            file_path="/path/to/audio",
            storage_id="storage123",
            text="test text",
            language="en",
            tags=["music", "podcast"],
            last_updated="2023-01-01T12:00:00+00:00",
        )

    def test_to_dto_with_valid_audio(self):
        result = self.mapper.to_dto(self.mock_audio)

        self.assertEqual(result.id, self.mock_audio.id)
        self.assertEqual(result.record_name, self.mock_audio.record_name)
        self.assertEqual(result.file_path, self.mock_audio.file_path)
        self.assertEqual(result.storage_id, self.mock_audio.storage_id)
        self.assertEqual(result.text, self.mock_audio.text)
        self.assertEqual(result.language, self.mock_audio.language)
        self.assertEqual(result.tags, self.mock_audio.tags)
        self.assertEqual(result.last_updated, "2023-01-01T12:00:00+00:00")

    def test_from_dto_creates_audio_record(self):
        self.mock_factory.create_audio.return_value = self.mock_audio

        self.mapper.from_dto(self.test_dto)

        self.mock_factory.create_audio.assert_called_once_with(
            file_name=self.test_dto.record_name,
            file_path=self.test_dto.file_path,
            storage_id=self.test_dto.storage_id,
            text=self.test_dto.text,
            language=self.test_dto.language,
        )


if __name__ == "__main__":
    unittest.main()
