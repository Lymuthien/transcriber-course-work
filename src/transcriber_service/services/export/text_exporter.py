from .formats.docx_exporter import DocxExporter
from .formats.iexporter import IExporter


class TextExporter:
    def __init__(self):
        self.__exporters: dict[str, IExporter] = {
            'docx': DocxExporter()
        }

    def export_text(self,
                    content: str,
                    output_dir: str,
                    filename: str,
                    file_format: str) -> None:

        if file_format not in self.__exporters:
            raise ValueError(f"Unsupported format: {file_format}")

        exporter = self.__exporters[file_format]
        output_path = f"{output_dir}/{filename}.{exporter.file_extension}"
        exporter.export(content, output_path)

