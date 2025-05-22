import unittest
from unittest.mock import MagicMock
from pydantic import BaseModel

from transcriber_service.application.serialization import (
    EntityMapperFactory,
    SerializerAdapter,
    UserDTO,
)
from transcriber_service.domain.interfaces import ISerializer


class TestSerializerAdapter(unittest.TestCase):
    def setUp(self):
        self.base_serializer = MagicMock(spec=ISerializer)
        self.entity_mapper_factory = MagicMock(spec=EntityMapperFactory)

        self.serializer = SerializerAdapter(
            base_serializer=self.base_serializer,
            entity_mapper_factory=self.entity_mapper_factory,
        )

    def test_serialize_with_entity(self):
        entity = MagicMock()
        entity.__class__.__name__ = "AuthUser"

        serializer_mock = MagicMock()
        dto = MagicMock(spec=UserDTO)
        dto.model_dump.return_value = {"id": 1, "entity_type": "authuser"}

        self.entity_mapper_factory.get_serializer.return_value = serializer_mock
        serializer_mock.to_dto.return_value = dto

        self.serializer.serialize(entity)

        self.entity_mapper_factory.get_serializer.assert_called_once_with("authuser")
        serializer_mock.to_dto.assert_called_once_with(entity)
        self.base_serializer.serialize.assert_called_once_with(
            {"id": 1, "entity_type": "authuser"}
        )

    def test_serialize_with_list(self):
        entity = MagicMock()
        entity.__class__.__name__ = "AuthUser"

        serializer_mock = MagicMock()
        dto = MagicMock(spec=UserDTO)
        dto.model_dump.return_value = {"id": 1, "entity_type": "authuser"}

        self.entity_mapper_factory.get_serializer.return_value = serializer_mock
        serializer_mock.to_dto.return_value = dto

        self.serializer.serialize([entity, entity])

        self.entity_mapper_factory.get_serializer.assert_called_with("authuser")
        self.assertEqual(serializer_mock.to_dto.call_count, 2)
        self.base_serializer.serialize.assert_called_once_with(
            [
                {"id": 1, "entity_type": "authuser"},
                {"id": 1, "entity_type": "authuser"},
            ],
        )

    def test_serialize_non_entity(self):
        obj = {"key": "value"}
        self.base_serializer.serialize.return_value = '{"key": "value"}'

        result = self.serializer.serialize(obj)

        self.base_serializer.serialize.assert_called_once_with(obj)
        self.assertEqual(result, '{"key": "value"}')

    def test_deserialize_non_entity(self):
        data = '{"key": "value"}'
        deserialized_data = {"key": "value"}

        self.base_serializer.deserialize.return_value = deserialized_data

        result = self.serializer.deserialize(data)

        self.base_serializer.deserialize.assert_called_once_with(data)
        self.assertEqual(result, {"key": "value"})

    def test_extension_property(self):
        self.base_serializer.extension = "json"
        self.assertEqual(self.serializer.extension, "json")

    def test_binary_property(self):
        self.base_serializer.binary = True
        self.assertEqual(self.serializer.binary, True)


if __name__ == "__main__":
    unittest.main()
