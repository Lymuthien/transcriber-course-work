from typing import Dict, Any

from ...domain import User, Storage, AudioRecord


class SerializationAdapter(object):
    def to_dict(self, obj: Any) -> dict[str, Any]:
        raise NotImplementedError

    def from_dict(self, data: dict[str, Any]) -> Any:
        raise NotImplementedError


class UserAdapter(SerializationAdapter):
    def to_dict(self, user: User) -> Dict[str, Any]:
        return {
            "type": user.__class__.__name__,
            "id": user.id,
            "email": user.email,
            "password_hash": user.password_hash,
            "registration_date": user.registration_date.isoformat(),
            "last_updated": user.last_updated.isoformat(),
            "is_blocked": user.is_blocked,
            "temp_password_hash": user.temp_password_hash,
        }

    def from_dict(self, data: Dict[str, Any]) -> User:
        cls = globals()[data["type"]]
        user = cls.__new__(cls)
        user.restore_state(data)

        return user


class StorageAdapter(SerializationAdapter):
    def to_dict(self, storage: Storage) -> dict[str, Any]:
        return {
            "type": storage.__class__.__name__,
            "id": storage.id,
            "user_id": storage.user_id,
            "audio_record_ids": storage.audio_record_ids,
        }

    def from_dict(self, data: dict[str, Any]) -> Storage:
        storage = Storage.__new__(Storage)
        storage.restore_state(data)

        return storage


class AudioRecordAdapter(SerializationAdapter):
    def to_dict(self, audio: AudioRecord) -> dict[str, Any]:
        return {
            "type": audio.__class__.__name__,
            "id": audio.id,
            "record_name": audio.record_name,
            "file_path": audio.file_path,
            "storage_id": audio.storage_id,
            "text": audio.text,
            "language": audio.language,
            "tags": audio.tags,
            "last_updated": audio.last_updated.isoformat(),
        }

    def from_dict(self, data: Dict[str, Any]) -> AudioRecord:
        audio = AudioRecord.__new__(AudioRecord)
        audio.restore_state(data)

        return audio


class SerializerFacade(object):
    def __init__(self, serializer):
        self._serializer = serializer
        self._adapters: dict[str, SerializationAdapter] = {
            "User": UserAdapter(),
            "Storage": StorageAdapter(),
            "AudioRecord": AudioRecordAdapter(),
        }

    def serialize(self, obj: Any) -> str:
        adapter = self._adapters[obj.__class__.__name__]
        data_dict = adapter.to_dict(obj)

        return self._serializer.serialize(data_dict)

    def deserialize(self, data: str) -> Any:
        data_dict = self._serializer.deserialize(data)
        adapter = self._adapters[data_dict["type"]]

        return adapter.from_dict(data_dict)
