from .formats.docx_exporter import DocxExporter
from .formats.iexporter import IExporter


class TextExporter(object):
    """Exporter of text (string) to different formats."""

    def __init__(self):
        self.__exporters: dict[str, IExporter] = {
            'docx': DocxExporter()
        }

    def export_text(self,
                    content: str,
                    output_dir: str,
                    filename: str,
                    file_format: str) -> None:
        """
        Export text (string) to format.

        :param content: Target text to export.
        :param output_dir: Target output directory.
        :param filename: Filename to save the exported text.
        :param file_format: Format to save the exported text (Now only 'docx').
        :raise ValueError: If format is not supported.
        """

        if file_format not in self.__exporters:
            raise ValueError(f"Unsupported format: {file_format}")

        exporter = self.__exporters[file_format]
        output_path = f"{output_dir}/{filename}.{exporter.file_extension}"
        exporter.export(content, output_path)
