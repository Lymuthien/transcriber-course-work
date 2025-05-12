import unittest
from unittest.mock import MagicMock

from transcriber_service.domain.interfaces import IAudioRecord
from transcriber_service.domain.services.audio_search_service import AudioSearchService


class TestAudioSearchService(unittest.TestCase):
    def setUp(self):
        self.record1 = MagicMock(spec=IAudioRecord)
        self.record1.tags = ["music", "jazz", "instrumental"]
        self.record1.record_name = "Jazz Night"

        self.record2 = MagicMock(spec=IAudioRecord)
        self.record2.tags = ["music", "rock", "live"]
        self.record2.record_name = "Rock Concert"

        self.record3 = MagicMock(spec=IAudioRecord)
        self.record3.tags = ["podcast", "interview"]
        self.record3.record_name = "Tech Talk"

        self.records = (self.record1, self.record2, self.record3)

    def test_search_by_tags_any_match(self):
        result = AudioSearchService.search_by_tags(self.records, ["jazz", "podcast"])
        self.assertEqual(len(result), 2)
        self.assertIn(self.record1, result)
        self.assertIn(self.record3, result)

    def test_search_by_tags_all_match(self):
        result = AudioSearchService.search_by_tags(
            self.records, ["music", "live"], match_all=True
        )
        self.assertEqual(len(result), 1)
        self.assertIn(self.record2, result)

    def test_search_by_tags_case_insensitive(self):
        result = AudioSearchService.search_by_tags(self.records, ["JAZZ", "ROCK"])
        self.assertEqual(len(result), 2)
        self.assertIn(self.record1, result)
        self.assertIn(self.record2, result)

    def test_search_by_tags_no_matches(self):
        result = AudioSearchService.search_by_tags(self.records, ["nonexistent"])
        self.assertEqual(len(result), 0)

    def test_search_by_name_exact_match(self):
        result = AudioSearchService.search_by_name(self.records, "Rock Concert")
        self.assertEqual(len(result), 1)
        self.assertIn(self.record2, result)

    def test_search_by_name_case_insensitive(self):
        result = AudioSearchService.search_by_name(self.records, "jazz night")
        self.assertEqual(len(result), 1)
        self.assertIn(self.record1, result)

    def test_search_by_name_partial_match_fails(self):
        result = AudioSearchService.search_by_name(self.records, "Rock")
        self.assertEqual(len(result), 0)

    def test_search_by_name_no_matches(self):
        result = AudioSearchService.search_by_name(self.records, "Nonexistent")
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
