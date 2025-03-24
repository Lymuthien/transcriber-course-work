import unittest

from transcriber_service.services.export.text_exporter import TextExporter


class TestTextExporter(unittest.TestCase):
    def setUp(self):
        self.text_exporter = TextExporter()

    def test_export_text_incorrect_file_format_raises_error(self):
        with self.assertRaises(ValueError):
            self.text_exporter.export_text('', '', '', '')

if __name__ == '__main__':
    unittest.main()
