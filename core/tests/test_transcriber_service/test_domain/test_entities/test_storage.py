import unittest

from transcriber_service.domain import Storage

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.user_id = '123'
        self.storage = Storage(user_id=self.user_id)

    def test_id_returns_string(self):
        self.assertEqual(type(self.storage.id), str)

    def test_user_id_returns_correct_string(self):
        self.assertEqual(self.storage.user_id, self.user_id)

    def test_audio_record_ids_returns_empty_list(self):
        self.assertEqual(self.storage.audio_record_ids, [])

    def test_add_audio_record(self):
        record_id = '456'
        self.storage.add_audio_record(record_id)
        self.assertEqual(self.storage.audio_record_ids, [record_id])

    def test_add_audio_record_dont_repeat(self):
        record_id = '456'
        self.storage.add_audio_record(record_id)
        self.storage.add_audio_record(record_id)
        self.assertEqual(self.storage.audio_record_ids, [record_id])

    def test_remove_audio_record(self):
        record_id = '789'
        self.storage.add_audio_record(record_id)
        self.storage.remove_audio_record(record_id)
        self.assertTrue(record_id not in self.storage.audio_record_ids)

    def test_remove_audio_record_raises_error_if_record_does_not_exist(self):
        record_id = '888'
        with self.assertRaises(ValueError):
            self.storage.remove_audio_record(record_id)

if __name__ == '__main__':
    unittest.main()
