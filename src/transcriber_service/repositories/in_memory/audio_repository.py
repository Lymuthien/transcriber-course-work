from typing import Dict

from .local_file_manager import LocalPickleFileManager
from ...interfaces.iaudio_record import IAudioRecord
from ...interfaces.iaudio_repository import IAudioRepository
from ...interfaces.ifile_manager import IFileManager
from ...interfaces.istorage_repository import IStorageRepository


class LocalAudioRepository(IAudioRepository):
    def __init__(self, storage_repository: IStorageRepository, data_dir: str,
                 file_manager: IFileManager = LocalPickleFileManager) -> None:
        """
        Create local audio repository.

        :type storage_repository: IStorageRepository.
        :param data_dir: Directory to store local audio data.
        """
        self.__manager = file_manager
        self.__records: Dict[str, IAudioRecord] = {}
        self.__storage_repository = storage_repository
        self.__dir = data_dir

        try:
            self.__records = file_manager.load(self.__dir)
        except:
            pass

    def get_by_storage(self, storage_id: str) -> tuple[IAudioRecord, ...]:
        """Return list of audio records by storage id."""
        return tuple(r for r in self.__records.values() if r.storage_id == storage_id)

    def get_by_id(self, record_id: str) -> IAudioRecord | None:
        """Return audio record by id if it exists else None."""

        return self.__records.get(record_id)

    def search_by_tags(self, storage_id: str, tags: list[str], match_all: bool = False) -> tuple[IAudioRecord, ...]:
        """
        Search audio records from storage by tags.

        :param storage_id: ID of target storage.
        :param tags: List of tags to search for.
        :param match_all: True if audio record must contain all tags.
        :return: Tuple of audio records.
        """

        tags = list(map(lambda s: s.lower(), tags))
        records = self.get_by_storage(storage_id)

        def matches(record: IAudioRecord):
            if match_all:
                return all(tag in record.tags for tag in tags)
            else:
                return any(tag in record.tags for tag in tags)

        return tuple(record for record in records if matches(record))

    def search_by_name(self, storage_id: str, name: str) -> tuple[IAudioRecord, ...]:
        """
        Search audio records from storage by record name.

        :param storage_id: ID of target storage.
        :param name: Record name.
        :return: Tuple of audio records.
        """

        records = self.get_by_storage(storage_id)
        name = name.lower()

        return tuple(record for record in records if record.record_name.lower() == name)

    def add(self, record: IAudioRecord) -> None:
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
            self.__manager.save(self.__records, self.__dir)


    def update(self, record: IAudioRecord) -> None:
        """
        Update audio record from repository with new value.

        :param record: new value of audio record.
        :raise ValueError: If audio record does not exist.
        """

        if record.id not in self.__records:
            raise ValueError('Record not found.')
        self.__records[record.id] = record
        self.__manager.save(self.__records, self.__dir)

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
        self.__manager.save(self.__records, self.__dir)
