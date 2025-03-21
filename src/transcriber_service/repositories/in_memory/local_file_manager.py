import pickle
from pathlib import Path

from ..interfaces.ifile_manager import IFileManager


class LocalFileManager(IFileManager):
    @staticmethod
    def save(data,
             filename: str) -> None:
        """Save data to file"""
        try:
            file_path = Path(filename)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            serialized_data = pickle.dumps(data)
            with open(filename, 'wb') as f:
                f.write(serialized_data)
        except Exception as e:
            raise Exception(f"Save failed: {str(e)}")

    @staticmethod
    def load(filename: str):
        """Load data from file"""
        try:
            with open(filename, 'rb') as f:
                serialized_data = pickle.loads(f.read())
                return serialized_data
        except Exception as e:
            raise Exception(f"Load failed: {str(e)}")
