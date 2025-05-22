import unittest
from unittest.mock import MagicMock
from transcriber_service.domain.interfaces import (
    IAudioRepository,
    IAudioRecord,
    ITranscriber,
    ITextExporter,
    IStopwordsRemover,
)
from transcriber_service.domain.factories import AudioRecordFactory
from transcriber_service.application.serialization.audio_mapper import (
    AudioRecordDTO,
    AudioRecordMapper,
)
from transcriber_service.domain.services.audio_search_service import AudioSearchService
from transcriber_service.application.services.audio_service import (
    AudioRecordService,
    AudioTagService,
    AudioTextService,
)


class TestAudioRecordService(unittest.TestCase):
    def setUp(self):
        self.repo = MagicMock(spec=IAudioRepository)
        self.transcriber = MagicMock(spec=ITranscriber)
        self.audio_factory = MagicMock(spec=AudioRecordFactory)
        self.search_service = MagicMock(spec=AudioSearchService)
        self.mapper = MagicMock(spec=AudioRecordMapper)

        self.service = AudioRecordService(self.repo, self.transcriber)
        self.service._audio_factory = self.audio_factory
        self.service._search_service = self.search_service
        self.service.mapper = self.mapper

    def test_create_audio_valid(self):
        content = b"audio_data"
        self.transcriber.transcribe.return_value = ("transcribed_text", "en")
        audio_record = MagicMock(spec=IAudioRecord)
        self.audio_factory.create_audio.return_value = audio_record

        result = self.service.create_audio(
            file_name="test.mp3",
            content=content,
            file_path="/path/test.mp3",
            storage_id="storage_1",
            language="en",
            max_speakers=2,
            main_theme="meeting",
        )

        self.transcriber.transcribe.assert_called_once_with(content, "en", 2, "meeting")
        self.audio_factory.create_audio.assert_called_once_with(
            "test.mp3", "/path/test.mp3", "storage_1", "transcribed_text", "en"
        )
        self.repo.add.assert_called_once_with(audio_record)
        self.assertEqual(result, audio_record)

    def test_create_audio_too_large(self):
        content = b"a" * (10 * 1024 * 1024 + 1)
        with self.assertRaises(Exception) as cm:
            self.service.create_audio(
                file_name="test.mp3",
                content=content,
                file_path="/path/test.mp3",
                storage_id="storage_1",
            )
        self.assertEqual(str(cm.exception), "Audio file too large.")
        self.transcriber.transcribe.assert_not_called()

    def test_get_records_found(self):
        records = [MagicMock(spec=IAudioRecord), MagicMock(spec=IAudioRecord)]
        self.repo.get_by_storage.return_value = records

        result = self.service.get_records("storage_1")

        self.repo.get_by_storage.assert_called_once_with("storage_1")
        self.assertEqual(result, records)

    def test_get_records_not_found(self):
        self.repo.get_by_storage.return_value = None

        result = self.service.get_records("storage_1")

        self.repo.get_by_storage.assert_called_once_with("storage_1")
        self.assertIsNone(result)

    def test_get_by_id_found(self):
        record = MagicMock(spec=IAudioRecord)
        self.repo.get_by_id.return_value = record

        result = self.service.get_by_id("record_1")

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertEqual(result, record)

    def test_get_by_id_not_found(self):
        self.repo.get_by_id.return_value = None

        result = self.service.get_by_id("record_1")

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertIsNone(result)

    def test_search_by_tags(self):
        records = [MagicMock(spec=IAudioRecord), MagicMock(spec=IAudioRecord)]
        matching_records = [records[0]]
        self.repo.get_by_storage.return_value = records
        self.search_service.search_by_tags.return_value = matching_records
        dto = MagicMock(spec=AudioRecordDTO)
        self.mapper.to_dto.return_value = dto

        result = self.service.search_by_tags(
            "storage_1", ["tag1", "tag2"], match_all=True
        )

        self.repo.get_by_storage.assert_called_once_with("storage_1")
        self.search_service.search_by_tags.assert_called_once_with(
            records, ["tag1", "tag2"], True
        )
        self.mapper.to_dto.assert_called_once_with(matching_records[0])
        self.assertEqual(result, [dto])

    def test_search_by_name(self):
        records = [MagicMock(spec=IAudioRecord), MagicMock(spec=IAudioRecord)]
        matching_records = [records[1]]
        self.repo.get_by_storage.return_value = records
        self.search_service.search_by_name.return_value = matching_records
        dto = MagicMock(spec=AudioRecordDTO)
        self.mapper.to_dto.return_value = dto

        result = self.service.search_by_name("storage_1", "test.mp3")

        self.repo.get_by_storage.assert_called_once_with("storage_1")
        self.search_service.search_by_name.assert_called_once_with(records, "test.mp3")
        self.mapper.to_dto.assert_called_once_with(matching_records[0])
        self.assertEqual(result, [dto])


class TestAudioTagService(unittest.TestCase):
    def setUp(self):
        self.repo = MagicMock(spec=IAudioRepository)
        self.service = AudioTagService(self.repo)

    def test_add_tag_to_record_found(self):
        record = MagicMock(spec=IAudioRecord)
        self.repo.get_by_id.return_value = record

        self.service.add_tag_to_record("record_1", "tag1")

        self.repo.get_by_id.assert_called_once_with("record_1")
        record.add_tag.assert_called_once_with("tag1")
        self.repo.update.assert_called_once_with(record)

    def test_add_tag_to_record_not_found(self):
        self.repo.get_by_id.return_value = None

        with self.assertRaises(ValueError) as cm:
            self.service.add_tag_to_record("record_1", "tag1")

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertEqual(str(cm.exception), "Record not found")
        self.repo.update.assert_not_called()

    def test_remove_tag_from_record_found(self):
        record = MagicMock(spec=IAudioRecord)
        self.repo.get_by_id.return_value = record

        self.service.remove_tag_from_record("record_1", "tag1")

        self.repo.get_by_id.assert_called_once_with("record_1")
        record.remove_tag.assert_called_once_with("tag1")
        self.repo.update.assert_called_once_with(record)

    def test_remove_tag_from_record_not_found(self):
        self.repo.get_by_id.return_value = None

        with self.assertRaises(ValueError) as cm:
            self.service.remove_tag_from_record("record_1", "tag1")

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertEqual(str(cm.exception), "Record not found")
        self.repo.update.assert_not_called()

    def test_remove_tag_from_record_tag_not_found(self):
        record = MagicMock(spec=IAudioRecord)
        self.repo.get_by_id.return_value = record
        record.remove_tag.side_effect = ValueError("Tag not found")

        self.service.remove_tag_from_record("record_1", "tag1")

        self.repo.get_by_id.assert_called_once_with("record_1")
        record.remove_tag.assert_called_once_with("tag1")
        self.repo.update.assert_not_called()


class TestAudioTextService(unittest.TestCase):
    def setUp(self):
        self.repo = MagicMock(spec=IAudioRepository)
        self.export_service = MagicMock(spec=ITextExporter)
        self.stopwords_remover = MagicMock(spec=IStopwordsRemover)
        self.service = AudioTextService(
            self.repo, self.export_service, self.stopwords_remover
        )

    def test_export_record_text_found(self):
        record = MagicMock(spec=IAudioRecord)
        record.text = "text content"
        record.record_name = "test.mp3"
        self.repo.get_by_id.return_value = record

        self.service.export_record_text("record_1", "/output", "txt")

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.export_service.export_text.assert_called_once_with(
            "text content", "/output", "test.mp3", "txt"
        )

    def test_export_record_text_not_found(self):
        self.repo.get_by_id.return_value = None

        with self.assertRaises(ValueError) as cm:
            self.service.export_record_text("record_1", "/output", "txt")

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertEqual(str(cm.exception), "Audio record not found")
        self.export_service.export_text.assert_not_called()

    def test_remove_stopwords_supported_language(self):
        record = MagicMock(spec=IAudioRecord)
        record.language = "russian"
        record.text = "original text"
        self.repo.get_by_id.return_value = record
        self.stopwords_remover.remove_stopwords.return_value = "cleaned text"

        self.service.remove_stopwords(
            "record_1", remove_swear_words=True, go_few_times=False
        )

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.stopwords_remover.remove_stopwords.assert_called_once_with(
            "original text", True, False
        )
        self.assertEqual(record.text, "cleaned text")
        self.repo.update.assert_called_once_with(record)

    def test_remove_stopwords_unsupported_language(self):
        record = MagicMock(spec=IAudioRecord)
        record.language = "english"
        self.repo.get_by_id.return_value = record

        with self.assertRaises(ValueError) as cm:
            self.service.remove_stopwords("record_1")

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertEqual(str(cm.exception), "Unsupported language: english")
        self.stopwords_remover.remove_stopwords.assert_not_called()

    def test_remove_stopwords_not_found(self):
        self.repo.get_by_id.return_value = None

        with self.assertRaises(ValueError) as cm:
            self.service.remove_stopwords("record_1")

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertEqual(str(cm.exception), "Audio record not found")
        self.stopwords_remover.remove_stopwords.assert_not_called()

    def test_remove_words_supported_language(self):
        record = MagicMock(spec=IAudioRecord)
        record.language = "ru"
        record.text = "original text"
        self.repo.get_by_id.return_value = record
        self.stopwords_remover.remove_words.return_value = "cleaned text"

        self.service.remove_words("record_1", ["word1", "word2"])

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.stopwords_remover.remove_words.assert_called_once_with(
            "original text", ["word1", "word2"]
        )
        self.assertEqual(record.text, "cleaned text")
        self.repo.update.assert_called_once_with(record)

    def test_remove_words_unsupported_language(self):
        record = MagicMock(spec=IAudioRecord)
        record.language = "en"
        self.repo.get_by_id.return_value = record

        with self.assertRaises(ValueError) as cm:
            self.service.remove_words("record_1", ["word1"])

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertEqual(str(cm.exception), "Unsupported language: en")
        self.stopwords_remover.remove_words.assert_not_called()

    def test_remove_words_not_found(self):
        self.repo.get_by_id.return_value = None

        with self.assertRaises(ValueError) as cm:
            self.service.remove_words("record_1", ["word1"])

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertEqual(str(cm.exception), "Audio record not found")
        self.stopwords_remover.remove_words.assert_not_called()

    def test_change_record_name_found(self):
        record = MagicMock(spec=IAudioRecord)
        self.repo.get_by_id.return_value = record

        self.service.change_record_name("record_1", "new_name.mp3")

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertEqual(record.record_name, "new_name.mp3")
        self.repo.update.assert_called_once_with(record)

    def test_change_record_name_not_found(self):
        self.repo.get_by_id.return_value = None

        with self.assertRaises(ValueError) as cm:
            self.service.change_record_name("record_1", "new_name.mp3")

        self.repo.get_by_id.assert_called_once_with("record_1")
        self.assertEqual(str(cm.exception), "Record not found")
        self.repo.update.assert_not_called()


if __name__ == "__main__":
    unittest.main()
