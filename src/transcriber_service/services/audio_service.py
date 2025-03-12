from .processing import ITranscribeProcessor
from ..domain import AudioRecord, Tag, RecordTag, TagException


class AudioService:
    """
    Service class for managing audio records and their lifecycle operations.

    Provides functionality to create, store, and retrieve audio records with optional
    transcription processing.
    """

    def __init__(self):
        self.__audio_records = []

    def create_audio(self,
                     file_name: str,
                     content: bytes,
                     file_path: str,
                     storage_id: str,
                     transcribe_processor: ITranscribeProcessor
                     ) -> AudioRecord:
        """
        Create AudioRecord instance with basic metadata and do transcription into text with given transcribe service.

        :param file_name: Name of audio file.
        :param content: Content of audio file (mp3).
        :param file_path: Full path to audio file in some storage directory (not user storage).
        :param storage_id: Storage id of audio file.
        :param transcribe_processor: Instance of transcribe_processor.

        Note: The audio record will be automatically added to the service's internal storage
        """
        audio = AudioRecord(file_name, content, file_path, storage_id, transcribe_processor)
        self.__audio_records.append(audio)
        return audio

    @property
    def audio_records(self) -> list:
        """Gets all stored audio records."""
        return self.__audio_records

    def get_records(self, storage_id: str) -> tuple | None:
        """
        Retrieves audio record by its storage container ID.

        :param storage_id: Storage id of audio file.
        :return: Tuple of audio records if it is found else None.
        """
        return tuple(record for record in self.__audio_records if record.storage_id == storage_id)


class TagService(object):
    def __init__(self):
        self.__tags: list[Tag] = []
        self.__record_tags: list[RecordTag] = []

    def get_tag(self, tag_id: str):
        pass

    def add_tag_to_record(self, tag_name: str, record_id: str) -> None:
        tag_id = self._find_tag_id(tag_name)

        if tag_id is not None:
            if self._find_tag_record(tag_id, record_id):
                raise TagException('Tag already exists.')
        else:
            tag_id = self._create_tag_id(tag_name)

        self.__record_tags.append(RecordTag(tag_id, record_id))

    def remove_tag_from_record(self, tag_name: str, record_id: str) -> None:
        tag_id = self._find_tag_id(tag_name)
        if not tag_id:
            raise TagException('Tag not found.')

        record_tag = self._find_tag_record(tag_id, record_id)
        if not record_tag:
            raise TagException('There is no audio record with that tag.')

        self.__record_tags.remove(record_tag)

    def find_records_by_tag(self, tag_name: str):
        tag_id = self._find_tag_id(tag_name)
        if not tag_id:
            raise TagException('Tag not found.')

        return tuple(self._find_records(tag_id))

    def find_tags_by_record(self, record_id: str) -> tuple:
        return tuple(record_tag.tag_id for record_tag in self.__record_tags if record_tag.record_id == record_id)

    def _find_tag_id(self, tag_name: str) -> str | None:
        for tag in self.__tags:
            if tag.name == tag_name.lower():
                return tag.id

    def _find_records(self, tag_id: str):
        return (record_tag.record_id for record_tag in self.__record_tags if record_tag.tag_id == tag_id)

    def _create_tag_id(self, tag_name: str) -> str:
        self.__tags.append(Tag(tag_name.lower()))
        return self.__tags[-1].id

    def _find_tag_record(self, tag_id: str, record_id) -> RecordTag | None:
        for record_tag in self.__record_tags:
            if record_tag.tag_id == tag_id and record_tag.record_id == record_id:
                return record_tag
