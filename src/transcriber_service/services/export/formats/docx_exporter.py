from docx import Document
from .iexporter import IExporter

class DocxExporter(IExporter):
    @property
    def file_extension(self) -> str:
        return "docx"

    def export(self, content: str, output_path: str) -> None:
        doc = Document()
        doc.add_paragraph(content)
        doc.save(output_path)