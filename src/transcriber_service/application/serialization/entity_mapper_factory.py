from typing import Dict
from ...domain.interfaces import IMapper
from .user_mapper import UserMapper
from .storage_mapper import StorageMapper
from .audio_mapper import AudioRecordMapper


class EntityMapperFactory(object):
    def __init__(self):
        self._serializers: Dict[str, IMapper] = {
            "auth_user": UserMapper(),
            "admin": UserMapper(),
            "storage": StorageMapper(),
            "audio_record": AudioRecordMapper(),
        }

    def get_serializer(self, entity_type: str) -> IMapper:
        """
        Get serializer for an entity type.

        :param entity_type: Type of the entity (e.g., 'auth_user', 'storage').
        :return: IDictable serializer.
        :raises ValueError: If serializer is not found.
        """
        serializer = self._serializers.get(entity_type)
        if serializer is None:
            raise ValueError(f"No serializer found for entity type: {entity_type}")

        return serializer

    def register_serializer(self, entity_type: str, serializer: IMapper) -> None:
        """
        Register a new serializer for an entity type.

        :param entity_type: Type of the entity.
        :param serializer: Serializer implementing IDictable.
        :raises ValueError: If entity_type is invalid.
        """
        if not isinstance(serializer, IMapper):
            raise TypeError("Serializer must implement IMapper.")

        self._serializers[entity_type] = serializer
