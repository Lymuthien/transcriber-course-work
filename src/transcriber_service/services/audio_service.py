from .export.text_exporter import TextExporter
from .interfaces import IStopwordsRemover
from .natasha_stopwords_remover import NatashaStopwordsRemover
from .transcribe_processor import ITranscribeProcessor
from ..domain import AudioRecord
from ..repositories import IAudioRepository


class AudioService(object):
    """
    Service class for managing audio records and their lifecycle operations.

    Provides functionality to create and retrieve audio records with optional
    transcription processing.
    """

    def __init__(self, repo: IAudioRepository, stopwords_remover: IStopwordsRemover):
        self.__audio_repo = repo
        self.__exporter = TextExporter()
        self.__stopwords_remover = stopwords_remover

    def create_audio(self,
                     file_name: str,
                     content: bytes,
                     file_path: str,
                     storage_id: str,
                     transcribe_processor: ITranscribeProcessor,
                     language: str = None,
                     main_theme: str = None,
                     ) -> AudioRecord:
        """
        Create AudioRecord instance with basic metadata and do transcription into text with given transcribe service.

        :param file_name: Name of audio file.
        :param content: Content of audio file (mp3).
        :param file_path: Full path to audio file in some storage directory (not user storage).
        :param storage_id: Storage id of audio file.
        :param transcribe_processor: Instance of transcribe_processor.
        :param language: Language of audio file (defaults None).
        :param main_theme: Main theme of audio file (defaults None).
        :return: Created Audio Record.
        """

        audio = AudioRecord(file_name, content, file_path, storage_id, transcribe_processor, language, main_theme)
        self.__audio_repo.add(audio)
        return audio

    def get_records(self,
                    storage_id: str) -> tuple | None:
        """
        Retrieves audio record by its storage container ID.

        :param storage_id: Storage id of audio file.
        :return: Tuple of audio records if it is found else None.
        """

        return self.__audio_repo.get_by_storage(storage_id)

    def add_tag_to_record(self,
                          record_id: str,
                          tag: str) -> None:
        """
        Add tag to record by its ID.

        :param record_id: ID of audio record.
        :param tag: Name of tag to add.
        :raise ValueError: If tag is not found.
        """

        record = self.__audio_repo.get_by_id(record_id)
        if record:
            record.add_tag(tag)
            self.__audio_repo.update(record)
        else:
            raise ValueError('Record not found')

    def remove_tag_from_record(self,
                               record_id: str,
                               tag: str) -> None:
        """
        Remove tag from record by its ID and tag name.

        :param record_id: ID of audio record.
        :param tag: Name of tag to remove.
        :raise ValueError: If tag is not found.
        """

        record = self.__audio_repo.get_by_id(record_id)
        if record:
            try:
                record.remove_tag(tag)
                self.__audio_repo.update(record)
            except ValueError:
                pass
        else:
            raise ValueError('Record not found')

    def change_record_name(self,
                           record_id: str,
                           name: str) -> None:
        """Change name of record by its ID."""

        record = self.__audio_repo.get_by_id(record_id)

        record.record_name = name
        self.__audio_repo.update(record)

    def export_record_text(self,
                           record_id: str,
                           output_dir: str,
                           file_format: str) -> None:
        """
        Export text of audio record by its ID.

        :param record_id: ID of audio record.
        :param output_dir: Target directory of exported text (without file name).
        :param file_format: Format to export.
        :raise ValueError: If record is not found.
        """

        record = self.__audio_repo.get_by_id(record_id)
        if not record:
            raise ValueError('Audio record not found')

        self.__exporter.export_text(''.join(record.text), output_dir, record.record_name, file_format)
        # Do something with punctuation and spaces. After transcribe.

    def remove_stopwords(self,
                         record_id: str,
                         remove_swear_words: bool = True) -> None:
        """
        Remove stopwords from audio record by its ID.

        Only records with russian language supports removing.
        :param record_id: ID of audio record.
        :param remove_swear_words: True if swear words should be removed.
        :raise ValueError:
            If record is not found.
            If language is not supported.
        """

        record = self.__audio_repo.get_by_id(record_id)

        if not record:
            raise ValueError('Audio record not found')
        if record.language != 'ru' or record.language != 'russian':
            raise ValueError(f'Unsupported language: {record.language}')

        record.text = self.__stopwords_remover.remove_parasite_words(record.text, remove_swear_words)

    def remove_words(self,
                     record_id: str,
                     words: list | tuple) -> None:
        """
        Remove words from audio record by its ID with given words.

        Only records with russian language supports removing.
        :param record_id: ID of audio record.
        :param words: List or tuple of removing words.
        :raise ValueError:
            If record is not found.
            If language is not supported.
        """

        record = self.__audio_repo.get_by_id(record_id)

        if not record:
            raise ValueError('Audio record not found')
        if record.language != 'ru' or record.language != 'russian':
            raise ValueError(f'Unsupported language: {record.language}')

        record.text = self.__stopwords_remover.remove_words(record.text, words)
