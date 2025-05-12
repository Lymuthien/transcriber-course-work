import unittest
import json

from transcriber_service.infrastructure.serializers import JsonSerializer


class TestJsonSerializer(unittest.TestCase):
    def setUp(self):
        self.serializer = JsonSerializer()

    def test_serialize_valid_data(self):
        data = {"key": "value", "number": 42}
        result = self.serializer.serialize(data)

        self.assertIsInstance(result, str)
        expected = json.dumps(data)
        self.assertEqual(result, expected)

    def test_serialize_complex_data(self):
        data = {"list": [1, 2, 3], "nested": {"a": True, "b": None}, "string": "test"}
        result = self.serializer.serialize(data)

        self.assertIsInstance(result, str)
        expected = json.dumps(data)
        self.assertEqual(result, expected)

    def test_deserialize_valid_data(self):
        data = {"key": "value", "number": 42}
        serialized = json.dumps(data)
        result = self.serializer.deserialize(serialized)

        self.assertEqual(result, data)

    def test_deserialize_complex_data(self):
        data = {"list": [1, 2, 3], "nested": {"a": True, "b": None}, "string": "test"}
        serialized = json.dumps(data)
        result = self.serializer.deserialize(serialized)

        self.assertEqual(result, data)

    def test_deserialize_invalid_type(self):
        with self.assertRaises(TypeError) as cm:
            self.serializer.deserialize(b"not a string")

        self.assertEqual(str(cm.exception), "Data must be a string")

    def test_deserialize_empty_data(self):
        with self.assertRaises(ValueError) as cm:
            self.serializer.deserialize("")

        self.assertEqual(str(cm.exception), "Data cannot be empty")

    def test_deserialize_whitespace_data(self):
        with self.assertRaises(ValueError) as cm:
            self.serializer.deserialize("   ")

        self.assertEqual(str(cm.exception), "Data cannot be empty")

    def test_deserialize_invalid_json(self):
        with self.assertRaises(json.JSONDecodeError):
            self.serializer.deserialize("invalid json")

    def test_extension_property(self):
        self.assertEqual(self.serializer.extension, "json")

    def test_binary_property(self):
        self.assertFalse(self.serializer.binary)


if __name__ == "__main__":
    unittest.main()
