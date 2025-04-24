from typing import Dict, Any

from ...domain import User, Storage, AudioRecord, Admin, AuthUser
from ...interfaces.iserializer import ISerializer, IDictable


class DictUser(IDictable):
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


class DictStorage(IDictable):
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


class DictAudioRecord(IDictable):
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


class SerializerProxy(ISerializer):
    def __init__(self, serializer: ISerializer):
        self._serializer = serializer
        self._adapters: dict[str, IDictable] = {
            User.__name__: DictUser(),
            Admin.__name__: DictUser(),
            AuthUser.__name__: DictUser(),
            Storage.__name__: DictStorage(),
            AudioRecord.__name__: DictAudioRecord(),
        }

    def serialize(self, obj: Any) -> str:
        if isinstance(obj, (list, tuple, set)):
            data = tuple(self.serialize(el) for el in obj)
        elif isinstance(obj, dict):
            data = {key: self.serialize(val) for key, val in obj.items()}
        else:
            adapter = self._adapters.get(obj.__class__.__name__)
            data = adapter.to_dict(obj) if adapter else obj

        return self._serializer.serialize(data)

    def deserialize(self, data: str) -> Any:
        data = self._serializer.deserialize(data)

        if isinstance(data, (list, tuple, set)):
            return list(self.deserialize(el) for el in data)
        elif isinstance(data, dict):
            if data.get("type"):
                adapter = self._adapters.get(data.get("type"))
                return adapter.from_dict(data) if adapter else data
            else:
                return {key: self.deserialize(val) for key, val in data.items()}
        else:
            return data
