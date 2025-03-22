from docx import Document

from .iexporter import IExporter


class DocxExporter(IExporter):
    """Exporter of string to docx."""

    @property
    def file_extension(self) -> str:
        return 'docx'

    def export(self, content: str, output_path: str) -> None:
        """
        Export string to docx.

        :param content: Target text to export.
        :param output_path: Target output path.
        """
        doc = Document()
        doc.add_paragraph(content)
        doc.save(output_path)
