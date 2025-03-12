from .processing import ITranscribeProcessor
from ..domain import AudioRecord, Tag, RecordTag, TagExistsException


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

    def add_tag_to_record(self, tag_name: str, record_id: str):
        tag_id, create_flag = self._find_tag_id_or_create(tag_name)

        if not create_flag:
            if self._check_if_tag_record_exists(tag_id, record_id):
                raise TagExistsException('Tag already exists.')

        self.__record_tags.append(RecordTag(tag_id, record_id))

    def _find_tag_id_or_create(self, tag_name: str) -> tuple[str, bool]:
        create_flag = False
        tag_id = None

        for tag in self.__tags:
            if tag.name == tag_name:
                tag_id = tag.id
        if not tag_id:
            self.__tags.append(Tag(tag_name))
            tag_id = self.__tags[-1].id
            create_flag = True

        return tag_id, create_flag

    def _check_if_tag_record_exists(self, tag_id: str, record_id) -> bool:
        for record_tag in self.__record_tags:
            if record_tag.tag_id == tag_id and record_tag.record_id == record_id:
                return True
        return False
