import unittest
from unittest.mock import MagicMock, patch

from transcriber_service.application.serialization import (
    EntityMapperFactory,
    UserMapper,
    StorageMapper,
    AudioRecordMapper,
)
from transcriber_service.domain.interfaces import IMapper


class TestEntityMapperFactory(unittest.TestCase):
    def setUp(self):
        self.factory = EntityMapperFactory()

        self.mock_user_mapper = MagicMock(spec=UserMapper)
        self.mock_storage_mapper = MagicMock(spec=StorageMapper)
        self.mock_audio_mapper = MagicMock(spec=AudioRecordMapper)

    def test_get_serializer_existing_types(self):
        self.assertIsInstance(self.factory.get_serializer("authuser"), IMapper)
        self.assertIsInstance(self.factory.get_serializer("admin"), IMapper)
        self.assertIsInstance(self.factory.get_serializer("storage"), IMapper)
        self.assertIsInstance(self.factory.get_serializer("audiorecord"), IMapper)

    def test_get_serializer_non_existent_type(self):
        with self.assertRaises(ValueError) as context:
            self.factory.get_serializer("nonexistent")
        self.assertEqual(
            str(context.exception), "No serializer found for entity type: nonexistent"
        )

    def test_register_serializer_valid(self):
        new_mapper = MagicMock(spec=IMapper)
        self.factory.register_serializer("newtype", new_mapper)

        self.assertEqual(self.factory.get_serializer("newtype"), new_mapper)

    def test_register_serializer_invalid_mapper(self):
        with self.assertRaises(TypeError) as context:
            self.factory.register_serializer("invalid", "not a mapper")
        self.assertEqual(str(context.exception), "Serializer must implement IMapper.")

    def test_register_serializer_overwrite_existing(self):
        new_mapper = MagicMock(spec=UserMapper)

        self.factory.register_serializer("authuser", new_mapper)
        self.assertEqual(self.factory.get_serializer("authuser"), new_mapper)

    def test_register_serializer_empty_type(self):
        with self.assertRaises(ValueError):
            self.factory.register_serializer("", MagicMock(spec=IMapper))


if __name__ == "__main__":
    unittest.main()
