from os.path import exists
from typing import Dict, Optional

from .local_file_manager import LocalFileManager
from ..interfaces.iaudio_repository import IAudioRepository
from ..interfaces.istorage_repository import IStorageRepository
from ...domain.audio import AudioRecord


class LocalAudioRepository(IAudioRepository):
    def __init__(self, storage_repository: IStorageRepository, data_dir: str) -> None:
        """
        Create local audio repository.

        :type storage_repository: IStorageRepository.
        :param data_dir: Directory to store local audio data.
        """

        self.__records: Dict[str, AudioRecord] = {}
        self.__storage_repository = storage_repository
        self.__dir = data_dir

        if exists(self.__dir):
            self.__records = LocalFileManager.load(self.__dir)

    def get_by_storage(self, storage_id: str) -> tuple[AudioRecord, ...]:
        """Return list of audio records by storage id."""

        return tuple(r for r in self.__records.values() if r.storage_id == storage_id)

    def get_by_id(self, record_id: str) -> AudioRecord | None:
        """Return audio record by id if it exists else None."""

        return self.__records.get(record_id)

    def search_by_tags(self, storage_id: str, tags: list[str], match_all: bool = False) -> tuple[AudioRecord, ...]:
        """
        Search audio records from storage by tags.

        :param storage_id: ID of target storage.
        :param tags: List of tags to search for.
        :param match_all: True if audio record must contain all tags.
        :return: Tuple of audio records.
        """

        tags = list(map(lambda s: s.lower(), tags))
        records = self.get_by_storage(storage_id)

        def matches(record: AudioRecord):
            if match_all:
                return all(tag in record.tags for tag in tags)
            else:
                return any(tag in record.tags for tag in tags)

        return tuple(record for record in records if matches(record))

    def search_by_name(self, storage_id: str, name: str) -> tuple[AudioRecord, ...]:
        """
        Search audio records from storage by record name.

        :param storage_id: ID of target storage.
        :param name: Record name.
        :return: Tuple of audio records.
        """

        records = self.get_by_storage(storage_id)
        name = name.lower()

        return tuple(record for record in records if record.record_name.lower() == name)

    def add(self, record: AudioRecord) -> None:
        """
        Add audio record to repository.

        :raise ValueError: If audio record already exists.
        """

        if record.id in self.__records:
            raise ValueError('Record already exists.')

        storage = self.__storage_repository.get_by_id(record.storage_id)
        if storage:
            storage.add_audio_record(record.id)
            self.__storage_repository.update(storage)

        self.__records[record.id] = record
        LocalFileManager.save(self.__records, self.__dir)

    def update(self, record: AudioRecord) -> None:
        """
        Update audio record from repository with new value.

        :param record: new value of audio record.
        :raise ValueError: If audio record does not exist.
        """

        if record.id not in self.__records:
            raise ValueError('Record not found.')
        self.__records[record.id] = record
        LocalFileManager.save(self.__records, self.__dir)

    def delete(self, record_id: str) -> None:
        """
        Delete audio record from repository.

        :param record_id: ID of target audio record.
        :raise ValueError: If audio record does not exist.
        """

        record = self.__records.get(record_id)
        if not record:
            raise ValueError('Record not found.')

        storage = self.__storage_repository.get_by_id(record.storage_id)
        if storage:
            storage.remove_audio_record(record_id)
            self.__storage_repository.update(storage)

        del self.__records[record_id]
        LocalFileManager.save(self.__records, self.__dir)
