from datetime import datetime
from uuid import uuid4


class AudioRecord(object):
    """
    Represents an audio record entity with metadata and transcription capabilities.
    Performs transcription of audio files into text during initialization.
    """

    def __init__(self, file_name: str, content: bytes, file_path: str, storage_id: str):
        """
        Create AudioRecord instance with basic metadata and do transcription into text.

        :param file_name: Name of audio file.
        :param content: Content of audio file (mp3).
        :param file_path: Full path to audio file in some storage directory (not user storage).
        :param storage_id: Storage id of audio file.
        """
        self.__id = uuid4().hex
        self.__record_name = file_name
        self.__file_path = file_path
        self.__storage_id = storage_id
        self.__last_updated = datetime.now()
        self.__text = self._transcribe(content)

    @staticmethod
    def _transcribe(content: bytes = None) -> str:
        """
        Placeholder for audio transcription functionality.
        Use whisper model to transcribe audio file into text.

        :param content: Audio bytes to transcribe (not currently processed).
        :return: Transcription text.
        """
        return ""

    @property
    def id(self) -> str:
        return str(self.__id)

    @property
    def record_name(self) -> str:
        """Display name for the audio record."""
        return self.__record_name

    @record_name.setter
    def record_name(self, note_name: str):
        """Sets the display name for the audio record."""
        self.__record_name = note_name

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


class Tag(object):
    """Represents a named tag with a UUID."""

    def __init__(self, tag_name: str):
        self.__id = uuid4().hex
        self.__tag_name = tag_name

    @property
    def id(self) -> str:
        return str(self.__id)

    @property
    def tag_name(self) -> str:
        return self.__tag_name


class RecordTag(object):
    """Establishes many-to-many relationship between AudioRecords and Tags."""

    def __init__(self, tag_id: str, record_id: str):
        """Creates a relationship between specific Tag and AudioRecord with their id."""
        self.__tag_id = tag_id
        self.__record_id = record_id

    @property
    def tag_id(self) -> str:
        return self.__tag_id

    @property
    def record_id(self) -> str:
        return self.__record_id
