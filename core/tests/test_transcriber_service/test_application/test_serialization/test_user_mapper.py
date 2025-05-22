import unittest
from unittest.mock import MagicMock
from datetime import datetime

import pydantic_core

from transcriber_service.application.serialization import UserMapper, UserDTO
from transcriber_service.domain import Admin, AuthUser
from transcriber_service.domain.interfaces import IUser


class TestUserMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = UserMapper()

        self.user = MagicMock(spec=AuthUser)
        self.user.id = "1"
        self.user.email = "user@example.com"
        self.user.password_hash = "hash123"
        self.user.registration_date = datetime(2023, 1, 1, 12, 0)
        self.user.last_updated = datetime(2023, 1, 2, 12, 0)
        self.user.is_blocked = False
        self.user.temp_password_hash = None

        self.admin = MagicMock(spec=Admin)
        self.admin.id = "2"
        self.admin.email = "admin@example.com"
        self.admin.password_hash = "hash456"
        self.admin.registration_date = datetime(2023, 2, 1, 12, 0)
        self.admin.last_updated = datetime(2023, 2, 2, 12, 0)
        self.admin.is_blocked = True
        self.admin.temp_password_hash = "temp_hash"

    def test_to_dto_authuser(self):
        result = self.mapper.to_dto(self.user)

        self.assertIsInstance(result, UserDTO)
        self.assertEqual(result.entity_type, "authuser")
        self.assertEqual(result.id, "1")
        self.assertEqual(result.email, "user@example.com")
        self.assertEqual(result.password_hash, "hash123")
        self.assertEqual(result.registration_date, "2023-01-01T12:00:00")
        self.assertEqual(result.last_updated, "2023-01-02T12:00:00")
        self.assertEqual(result.is_blocked, False)
        self.assertIsNone(result.temp_password_hash)

    def test_to_dto_admin(self):
        result = self.mapper.to_dto(self.admin)

        self.assertIsInstance(result, UserDTO)
        self.assertEqual(result.entity_type, "admin")
        self.assertEqual(result.id, "2")
        self.assertEqual(result.email, "admin@example.com")
        self.assertEqual(result.password_hash, "hash456")
        self.assertEqual(result.registration_date, "2023-02-01T12:00:00")
        self.assertEqual(result.last_updated, "2023-02-02T12:00:00")
        self.assertEqual(result.is_blocked, True)
        self.assertEqual(result.temp_password_hash, "temp_hash")

    def test_to_dto_invalid_user(self):
        invalid_user = MagicMock()

        with self.assertRaises(TypeError) as cm:
            self.mapper.to_dto(invalid_user)

        self.assertEqual(str(cm.exception), "Object must be a IUser instance")

    def test_from_dto_authuser(self):
        dto = UserDTO(
            entity_type="authuser",
            id="1",
            email="user@example.com",
            password_hash="hash123",
            registration_date=datetime(2023, 1, 1, 12, 0).isoformat(),
            last_updated=datetime(2023, 1, 1, 12, 0).isoformat(),
            is_blocked=False,
            temp_password_hash=None,
        )

        result = self.mapper.from_dto(dto)

        self.assertEqual(result.id, "1")
        self.assertEqual(result.is_blocked, False)
        self.assertEqual(result.registration_date, datetime(2023, 1, 1, 12, 0))
        self.assertEqual(result.last_updated, datetime(2023, 1, 1, 12, 0))
        self.assertIsNone(result.temp_password_hash)

    def test_from_dto_admin_with_temp_password(self):
        dto = UserDTO(
            entity_type="admin",
            id="1",
            email="user@example.com",
            password_hash="hash123",
            registration_date=datetime(2023, 1, 1, 12, 0).isoformat(),
            last_updated=datetime(2023, 1, 1, 12, 0).isoformat(),
            is_blocked=True,
            temp_password_hash="None",
        )

        result = self.mapper.from_dto(dto)

        self.assertEqual(result.id, "1")
        self.assertEqual(result.is_blocked, True)
        self.assertEqual(result.registration_date, datetime(2023, 1, 1, 12, 0))
        self.assertEqual(result.last_updated, datetime(2023, 1, 1, 12, 0))
        self.assertIsNotNone(result.temp_password_hash)


if __name__ == "__main__":
    unittest.main()
