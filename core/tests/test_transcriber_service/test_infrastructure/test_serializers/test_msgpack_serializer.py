import unittest
import msgpack

from transcriber_service.infrastructure.serializers.msgpack_serializer import (
    MsgpackSerializer,
)


class TestMsgpackSerializer(unittest.TestCase):
    def setUp(self):
        self.serializer = MsgpackSerializer()

    def test_serialize_valid_data(self):
        data = {"key": "value", "number": 42}
        result = self.serializer.serialize(data)

        self.assertIsInstance(result, bytes)
        expected = msgpack.packb(data, use_bin_type=True)
        self.assertEqual(result, expected)

    def test_serialize_complex_data(self):
        data = {"list": [1, 2, 3], "nested": {"a": True, "b": None}, "bytes": b"test"}
        result = self.serializer.serialize(data)

        self.assertIsInstance(result, bytes)
        expected = msgpack.packb(data, use_bin_type=True)
        self.assertEqual(result, expected)

    def test_deserialize_valid_data(self):
        data = {"key": "value", "number": 42}
        serialized = msgpack.packb(data, use_bin_type=True)
        result = self.serializer.deserialize(serialized)

        self.assertEqual(result, data)

    def test_deserialize_complex_data(self):
        data = {"list": [1, 2, 3], "nested": {"a": True, "b": None}, "bytes": b"test"}
        serialized = msgpack.packb(data, use_bin_type=True)
        result = self.serializer.deserialize(serialized)

        self.assertEqual(result, data)

    def test_deserialize_invalid_type(self):
        with self.assertRaises(TypeError) as cm:
            self.serializer.deserialize("not bytes")

        self.assertEqual(str(cm.exception), "Data must be bytes")

    def test_deserialize_empty_data(self):
        with self.assertRaises(ValueError) as cm:
            self.serializer.deserialize(b"")

        self.assertEqual(str(cm.exception), "Data cannot be empty")

    def test_extension_property(self):
        self.assertEqual(self.serializer.extension, "msgpack")

    def test_binary_property(self):
        self.assertTrue(self.serializer.binary)


if __name__ == "__main__":
    unittest.main()
