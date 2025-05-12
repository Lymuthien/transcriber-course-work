import unittest
from unittest.mock import MagicMock

from transcriber_service.application.serialization import StorageMapper, StorageDTO
from transcriber_service.domain.factories import IStorageFactory
from transcriber_service.domain.interfaces import IStorage


class TestStorageMapper(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock(spec=IStorageFactory)

        self.mapper = StorageMapper(factory=self.factory)

        self.storage = MagicMock(spec=IStorage)
        self.storage.id = "1"
        self.storage.user_id = "user_123"
        self.storage.audio_record_ids = ["record_1", "record_2"]

    def test_to_dto_valid_storage(self):
        result = self.mapper.to_dto(self.storage)

        self.assertIsInstance(result, StorageDTO)
        self.assertEqual(result.entity_type, "storage")
        self.assertEqual(result.id, "1")
        self.assertEqual(result.user_id, "user_123")
        self.assertEqual(result.audio_record_ids, ["record_1", "record_2"])

    def test_to_dto_invalid_storage(self):
        invalid_storage = MagicMock()

        with self.assertRaises(TypeError) as cm:
            self.mapper.to_dto(invalid_storage)

        self.assertEqual(str(cm.exception), "Object must be a IStorage instance")

    def test_from_dto_valid_dto(self):
        dto = StorageDTO(
            entity_type="storage",
            id="1",
            user_id="user_123",
            audio_record_ids=["record_1", "record_2"],
        )

        created_storage = MagicMock(spec=IStorage)
        self.factory.create_storage.return_value = created_storage

        result = self.mapper.from_dto(dto)

        self.factory.create_storage.assert_called_once_with("user_123")
        created_storage.add_audio_record.assert_any_call("record_1")
        created_storage.add_audio_record.assert_any_call("record_2")
        self.assertEqual(created_storage.id, "1")
        self.assertEqual(result, created_storage)

    def test_from_dto_empty_audio_records(self):
        dto = StorageDTO(
            entity_type="storage", id="2", user_id="user_456", audio_record_ids=[]
        )

        created_storage = MagicMock(spec=IStorage)
        self.factory.create_storage.return_value = created_storage

        result = self.mapper.from_dto(dto)

        self.factory.create_storage.assert_called_once_with("user_456")
        created_storage.add_audio_record.assert_not_called()
        self.assertEqual(created_storage.id, "2")
        self.assertEqual(result, created_storage)


if __name__ == "__main__":
    unittest.main()
