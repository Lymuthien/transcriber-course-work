from typing import Dict, Optional
from ..interfaces.iaudio_repository import IAudioRepository
from ..interfaces.istorage_repository import IStorageRepository
from ...domain.audio import AudioRecord


class InMemoryAudioRepository(IAudioRepository):
    def __init__(self, storage_repository: IStorageRepository) -> None:
        self.__records: Dict[str, AudioRecord] = {}
        self.__storage_repository = storage_repository

    def get_by_storage(self, storage_id: str) -> tuple[AudioRecord, ...]:
        return tuple(r for r in self.__records.values() if r.storage_id == storage_id)

    def get_by_id(self, record_id: str) -> Optional[AudioRecord]:
        return self.__records.get(record_id)

    def add(self, record: AudioRecord) -> None:
        if record.id in self.__records:
            raise ValueError('Record already exists.')

        storage = self.__storage_repository.get_by_id(record.storage_id)
        if storage:
            storage.add_audio_record(record.id)
            self.__storage_repository.update(storage)

        self.__records[record.id] = record

    def update(self, record: AudioRecord) -> None:
        if record.id not in self.__records:
            raise ValueError('Record not found.')
        self.__records[record.id] = record

    def delete(self, record_id: str) -> None:
        record = self.__records.get(record_id)
        if not record:
            raise ValueError('Record not found.')

        storage = self.__storage_repository.get_by_id(record.storage_id)
        if storage:
            storage.remove_audio_record(record_id)
            self.__storage_repository.update(storage)

        del self.__records[record_id]