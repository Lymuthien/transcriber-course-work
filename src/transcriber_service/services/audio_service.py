from .processing import ITranscribeProcessor
from ..domain import AudioRecord
from ..repositories import IAudioRepository


class AudioService:
    """
    Service class for managing audio records and their lifecycle operations.

    Provides functionality to create and retrieve audio records with optional
    transcription processing.
    """

    def __init__(self, repo: IAudioRepository):
        self.__audio_repo = repo

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
        """

        audio = AudioRecord(file_name, content, file_path, storage_id, transcribe_processor)
        self.__audio_repo.add(audio)
        return audio

    # @property
    # def audio_records(self) -> list:
    #     """Gets all stored audio records."""
    #
    #     return self.__audio_records

    def get_records(self, storage_id: str) -> tuple | None:
        """
        Retrieves audio record by its storage container ID.

        :param storage_id: Storage id of audio file.
        :return: Tuple of audio records if it is found else None.
        """

        return self.__audio_repo.get_by_storage(storage_id)


