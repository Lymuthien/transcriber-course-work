import unittest
from unittest.mock import MagicMock

from transcriber_service.domain import AudioRecord
from transcriber_service.interfaces.iaudio_record import IAudioRecord
from transcriber_service.interfaces.iaudio_repository import IAudioRepository
from audio_transcriber.src.audio_transcribing.interfaces import ITranscribeProcessor, IStopwordsRemover
from transcriber_service.services import AudioService
from transcriber_service.services.export.text_exporter import TextExporter


class TestAudioService(unittest.TestCase):
    def setUp(self):
        self.mock_audio_repository = MagicMock(spec=IAudioRepository)
        self.mock_audio_repository.get_by_storage.return_value = None
        self.mock_audio_repository.get_by_id.return_value = None

        self.mock_stopwords_remover = MagicMock(spec=IStopwordsRemover)
        self.mock_exporter = MagicMock(spec=TextExporter)
        self.mock_transcribe_processor = MagicMock(spec=ITranscribeProcessor)
        self.mock_transcribe_processor.transcribe_audio.return_value = 'Какой-то текст на русском языке.', 'ru'

        self.audio_service = AudioService(repo=self.mock_audio_repository,
                                          stopwords_remover=self.mock_stopwords_remover,
                                          transcribe_processor=self.mock_transcribe_processor,
                                          exporter=self.mock_exporter)

    def test_create_audio(self):
        audio = self.audio_service.create_audio('name', b'bytes', 'path', 'id')
        self.assertEqual(type(audio), AudioRecord)

    def test_get_records(self):
        self.audio_service.get_records('lala')
        self.mock_audio_repository.get_by_storage.assert_called_once_with('lala')

    def test_add_tag_to_record_not_found_raises_error(self):
        with self.assertRaises(ValueError):
            self.audio_service.add_tag_to_record('', 'song')
        self.mock_audio_repository.get_by_id.assert_called_once_with('')

    def test_remove_tag_from_record_not_found_raises_error(self):
        with self.assertRaises(ValueError):
            self.audio_service.remove_tag_from_record('', 'song')
        self.mock_audio_repository.get_by_id.assert_called_once_with('')

    def test_change_record_name(self):
        mock_record = MagicMock(spec=IAudioRecord)
        self.mock_audio_repository.get_by_id.return_value = mock_record
        self.audio_service.change_record_name('', 'name')
        self.mock_audio_repository.get_by_id.assert_called_once_with('')
        self.mock_audio_repository.update.assert_called_once_with(mock_record)

    def test_export_record_text(self):
        mock_record = MagicMock(spec=IAudioRecord)
        self.mock_audio_repository.get_by_id.return_value = mock_record

        self.audio_service.export_record_text('', '', '')
        self.mock_audio_repository.get_by_id.assert_called_once_with('')
        self.mock_exporter.export_text.assert_called_once()

    def test_export_record_text_not_found_record_raises_error(self):
        with self.assertRaises(ValueError):
            self.audio_service.export_record_text('', '', '')

    def test_remove_stopwords(self):
        mock_record = MagicMock(spec=IAudioRecord)
        mock_record.language = 'ru'
        self.mock_audio_repository.get_by_id.return_value = mock_record

        self.audio_service.remove_stopwords('', True)
        self.mock_audio_repository.get_by_id.assert_called_once_with('')

    def test_remove_stopwords_not_found_raises_error(self):
        with self.assertRaises(ValueError):
            self.audio_service.remove_stopwords('')

    def test_remove_stopwords_incorrect_language_raises_error(self):
        mock_record = MagicMock(spec=IAudioRecord)
        mock_record.language = 'en'
        self.mock_audio_repository.get_by_id.return_value = mock_record

        with self.assertRaises(ValueError):
            self.audio_service.remove_stopwords('', True)

    def test_remove_words(self):
        mock_record = MagicMock(spec=IAudioRecord)
        mock_record.language = 'ru'
        self.mock_audio_repository.get_by_id.return_value = mock_record

        self.audio_service.remove_words('', ['lena'])
        self.mock_audio_repository.get_by_id.assert_called_once_with('')

    def test_remove_words_not_found_raises_error(self):
        with self.assertRaises(ValueError):
            self.audio_service.remove_words('', [])

    def test_remove_words_incorrect_language_raises_error(self):
        mock_record = MagicMock(spec=IAudioRecord)
        mock_record.language = 'en'
        self.mock_audio_repository.get_by_id.return_value = mock_record

        with self.assertRaises(ValueError):
            self.audio_service.remove_words('', [])


if __name__ == '__main__':
    unittest.main()
