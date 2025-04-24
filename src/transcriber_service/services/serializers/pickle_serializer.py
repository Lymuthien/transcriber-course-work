import pickle

from ...interfaces.iserializer import ISerializer


class PickleSerializer(ISerializer):
    def serialize(self, data) -> bytes:
        return pickle.dumps(data)

    def deserialize(self, data: bytes):
        return pickle.loads(data)

    @property
    def extension(self) -> str:
        return 'pickle'

    @property
    def binary(self) -> bool:
        return True
