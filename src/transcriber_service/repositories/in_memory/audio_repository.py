from typing import Dict, List
from ..interfaces.iaudio_repository import IAudioRepository
from ...domain.audio import AudioRecord


class InMemoryAudioRepository(IAudioRepository):
    def __init__(self):
        self._records: Dict[str, AudioRecord] = {}

    def get_by_storage(self, storage_id: str) -> tuple[AudioRecord, ...]:
        return tuple(r for r in self._records.values() if r.storage_id == storage_id)

    def add(self, record: AudioRecord) -> None:
        if record.id in self._records:
            raise ValueError('Record already exists.')
        self._records[record.id] = record

    def update(self, record: AudioRecord) -> None:
        if record.id not in self._records:
            raise ValueError('Record not found.')
        self._records[record.id] = record

    def delete(self, record_id: str) -> None:
        if record_id not in self._records:
            raise ValueError('Record not found.')
        del self._records[record_id]