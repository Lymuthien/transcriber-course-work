from typing import Dict, Any

from ...domain import Storage, AudioRecord
from ...interfaces.iserializer import ISerializer, IDictable
from ...interfaces.iuser import IUser


class UserSerializer(IDictable):
    def to_dict(self, user: IUser) -> Dict[str, Any]:
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

    def from_dict(self, data: Dict[str, Any]) -> IUser:
        cls = globals()[data["type"]]
        user = cls.__new__(cls)
        user.restore_state(data)

        return user


class StorageSerializer(IDictable):
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


class AudioRecordSerializer(IDictable):
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


class EntitySerializerFactory(object):
    def __init__(self):
        us = UserSerializer()
        self.__serializers: Dict[str, IDictable] = {
            "User": us,
            "AuthUser": us,
            "Admin": us,
            "Storage": StorageSerializer(),
            "AudioRecord": AudioRecordSerializer(),
        }

    def get_serializer(self, entity_type: str) -> IDictable | None:
        serializer = self.__serializers.get(entity_type)
        return serializer

    def register_serializer(self, entity_type: str, serializer: IDictable) -> None:
        """Register a new serializer for an entity type."""
        self.__serializers[entity_type] = serializer


class SerializerProxy(ISerializer):
    def __init__(
        self,
        serializer: ISerializer,
        entity_serializer_factory: EntitySerializerFactory,
    ):
        self.__base_serializer = serializer
        self.__serializer_factory = entity_serializer_factory

    def serialize(self, obj: Any) -> str:
        if isinstance(obj, (list, tuple, set)):
            data = tuple(self.serialize(el) for el in obj)
        elif isinstance(obj, dict):
            data = {key: self.serialize(val) for key, val in obj.items()}
        else:
            serializer = self.__serializer_factory.get_serializer(
                obj.__class__.__name__
            )
            data = serializer.to_dict(obj) if serializer else obj

        return self.__base_serializer.serialize(data)

    def deserialize(self, data: str) -> Any:
        data = self.__base_serializer.deserialize(data)

        if isinstance(data, (list, tuple, set)):
            return list(self.deserialize(el) for el in data)
        elif isinstance(data, dict):
            if data.get("type"):
                serializer = self.__serializer_factory.get_serializer(data["type"])
                return serializer.from_dict(data) if serializer else data
            else:
                return {key: self.deserialize(val) for key, val in data.items()}
        else:
            return data

    def extension(self) -> str:
        return self.__base_serializer.extension

    def binary(self) -> bool:
        return self.__base_serializer.binary
