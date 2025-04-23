from pathlib import Path

from ...interfaces.ifile_manager import IFileManager
from ...interfaces.iserializer import ISerializer


class LocalFileManager(IFileManager):
    @staticmethod
    def save(
        data, filename: str, binary: bool = True, serializer: ISerializer = None
    ) -> None:
        """Save data to file."""

        file_path = Path(filename)

        if serializer:
            data = serializer.serialize(data)

        with open(file_path, "wb" if binary else "w") as f:
            f.write(data)

    @staticmethod
    def load(filename: str, binary: bool = True, serializer: ISerializer = None):
        """Load data from file."""

        with open(filename, "rb" if binary else "r") as f:
            data = f.read()
            if serializer:
                data = serializer.deserialize(data)

            return data
