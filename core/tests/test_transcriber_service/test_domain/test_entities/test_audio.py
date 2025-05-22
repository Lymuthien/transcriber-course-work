import unittest

from transcriber_service.domain import AudioRecord


class TestAudioRecord(unittest.TestCase):
    def setUp(self):
        self.storage_id = "123"
        self.language = "ru"
        self.test_text = "Some text."
        self.name = "test.wav"

        self.record = AudioRecord(
            file_name=self.name,
            file_path="test/path",
            storage_id=self.storage_id,
            text=self.test_text,
            language=self.language,
        )

    def test_id_return_str_type(self):
        self.assertEqual(type(self.record.id), str)

    def test_text_return_str_type(self):
        self.assertEqual(type(self.record.text), str)

    def test_text_return_test_text(self):
        self.assertEqual(self.record.text, self.test_text)

    def test_text_set_works(self):
        self.record.text = test = "Other text."
        self.assertEqual(self.record.text, test)

    def test_language_return_ru_type(self):
        self.assertEqual(self.record.language, self.language)

    def test_tags_return_empy_list(self):
        self.assertEqual(self.record.tags, [])

    def test_add_tag_to_list(self):
        tag = "new tag"
        self.record.add_tag(tag)
        self.assertEqual(self.record.tags, [tag])

    def test_add_tag_repeating_dont_add_to_list(self):
        tag = "new tag"
        self.record.add_tag(tag)
        self.record.add_tag(tag)
        self.assertEqual(self.record.tags, [tag])

    def test_add_tag_makes_lower(self):
        tag = "OTHER tAg"
        self.record.add_tag(tag)
        self.assertEqual(self.record.tags[-1], tag.lower())

    def test_remove_tag(self):
        tag = "1"
        self.record.add_tag(tag)
        self.record.remove_tag(tag)
        self.assertTrue(tag not in self.record.tags)

    def test_remove_tag_any_case(self):
        tag = "loW"
        self.record.add_tag(tag)
        self.record.remove_tag(tag.upper())
        self.assertTrue(tag not in self.record.tags)

    def test_remove_tag_raises_error_if_tag_doesnt_exist(self):
        with self.assertRaises(ValueError):
            self.record.remove_tag("564687")

    def test_record_name_return_correct(self):
        self.assertEqual(self.record.record_name, self.name)

    def test_record_name_sets_correctly(self):
        self.record.record_name = name = "New.mp3"
        self.assertEqual(self.record.record_name, name)

    def test_storage_id_return_correct(self):
        self.assertEqual(self.record.storage_id, self.storage_id)


if __name__ == "__main__":
    unittest.main()
