import pickle

from transcriber_service.domain.interfaces.services.iserializer import ISerializer


class PickleSerializer(ISerializer):
    def serialize(self, data) -> bytes:
        return pickle.dumps(data)

    def deserialize(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError("Data must be bytes")
        if not data:
            raise ValueError("Data cannot be empty")

        return pickle.loads(data)

    @property
    def extension(self) -> str:
        return "pickle"

    @property
    def binary(self) -> bool:
        return True
