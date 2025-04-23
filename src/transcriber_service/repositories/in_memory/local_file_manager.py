import pickle
from pathlib import Path

from ...interfaces.ifile_manager import IFileManager
from ...interfaces.iserializer import ISerializer


class LocalPickleFileManager(IFileManager):
    """Local file manager for saving and loading files. Uses pickle serialization."""

    @staticmethod
    def save(data, filename: str) -> None:
        """Save data to file."""

        file_path = Path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        serialized_data = pickle.dumps(data)
        with open(filename, "wb") as f:
            f.write(serialized_data)

    @staticmethod
    def load(filename: str):
        """Load data from file."""

        with open(filename, "rb") as f:
            serialized_data = pickle.loads(f.read())
            return serialized_data


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
