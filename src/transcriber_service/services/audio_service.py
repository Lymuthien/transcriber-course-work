from .processing import ITranscribeProcessor
from ..domain import AudioRecord


class AudioService:
    def __init__(self):
        self.__audio_records = []

    def create_audio(self,
                     file_name: str,
                     content: bytes,
                     file_path: str,
                     storage_id: str,
                     transcribe_processor: ITranscribeProcessor
                     ) -> AudioRecord:
        audio = AudioRecord(file_name, content, file_path, storage_id, transcribe_processor)
        self.__audio_records.append(audio)
        return audio

    @property
    def audio_records(self) -> list:
        return self.__audio_records

    def get_record(self, storage_id: str) -> AudioRecord | None:
        for record in self.__audio_records:
            if record.storage_id == storage_id:
                return record