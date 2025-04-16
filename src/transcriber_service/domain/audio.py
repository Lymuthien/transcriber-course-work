from datetime import datetime
from uuid import uuid4

from ..audio_transcriber.interfaces import ITranscribeProcessor
from ..interfaces.iaudio_record import IAudioRecord


class AudioRecord(IAudioRecord):
    def __init__(self,
                 file_name: str,
                 content: bytes,
                 file_path: str,
                 storage_id: str,
                 transcribe_processor: ITranscribeProcessor,
                 language: str = None,
                 main_theme: str = None):
        """
        Create AudioRecord instance with basic metadata and do transcription into text with given transcribe service.

        :param file_name: Name of audio file.
        :param content: Content of audio file (mp3).
        :param file_path: Full path to audio file in some storage directory (not user storage).
        :param storage_id: Storage id of audio file.
        :param transcribe_processor: Instance of transcribe_processor.
        :param language: Language of audio file (defaults None).
        :param main_theme: Main theme of audio file (defaults None).
        """

        self.__id = uuid4().hex
        self.__record_name = file_name
        self.__file_path = file_path
        self.__storage_id = storage_id
        self.__last_updated = datetime.now()
        self.__text, self.__language  = transcribe_processor.transcribe_audio(content, language, main_theme)
        self.__tags = []

    @property
    def id(self) -> str:
        """Return ID of audio record."""

        return self.__id

    @property
    def text(self) -> str:
        """Return text of audio record."""

        return self.__text

    @text.setter
    def text(self, value: str) -> None:
        """Set text for audio record."""

        self.__text = value
        self.__last_updated = datetime.now()

    @property
    def language(self) -> str:
        """Return language of audio file."""

        return self.__language

    @property
    def tags(self) -> list:
        """Return tags of audio record."""

        return self.__tags.copy()

    def add_tag(self, tag_name: str) -> None:
        """Add tag to audio record. Saved in lower case."""

        if tag_name.lower() not in self.__tags:
            self.__tags.append(tag_name.lower())
            self.__last_updated = datetime.now()

    def remove_tag(self, tag_name: str) -> None:
        """
        Remove tag from audio record.

        :raise ValueError: If tag does not exist.
        """

        self.__tags.remove(tag_name.lower())
        self.__last_updated = datetime.now()

    @property
    def record_name(self) -> str:
        """Return name for the audio record."""

        return self.__record_name

    @record_name.setter
    def record_name(self,
                    note_name: str):
        """Sets the display name for the audio record."""

        self.__record_name = note_name
        self.__last_updated = datetime.now()

    @property
    def file_path(self) -> str:
        """Absolute filesystem path to the audio file."""

        return self.__file_path

    @property
    def storage_id(self) -> str:
        """Identifier of associated storage container."""

        return self.__storage_id

    @property
    def last_updated(self) -> datetime:
        """Timestamp of last modification in UTC."""

        return self.__last_updated