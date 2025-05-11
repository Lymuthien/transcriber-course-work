from pathlib import Path

from ...interfaces import IFileManager
from ...domain.interfaces import ISerializer


class LocalFileManager(IFileManager):
    @staticmethod
    def save(
        data, filename: str, binary: bool = True, serializer: ISerializer = None
    ) -> None:
        """Save data to file."""

        if serializer:
            filename = f"{filename}.{serializer.extension}"
            data = serializer.serialize(data)
            binary = serializer.binary

        file_path = Path(filename)

        with open(file_path, "wb" if binary else "w") as f:
            f.write(data)

    @staticmethod
    def load(filename: str, binary: bool = True, serializer: ISerializer = None):
        """Load data from file."""
        if serializer:
            filename = f"{filename}.{serializer.extension}"
            binary = serializer.binary

        with open(filename, "rb" if binary else "r") as f:
            data = f.read()

            return serializer.deserialize(data) if serializer else data
