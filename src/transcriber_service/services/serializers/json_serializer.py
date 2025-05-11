import json

from ...interfaces.iserializer import ISerializer


class JsonSerializer(ISerializer):
    def serialize(self, data) -> str:
        return json.dumps(data)

    def deserialize(self, data: str):
        data_dict = json.loads(data)
        return data_dict

    @property
    def extension(self) -> str:
        return "json"

    @property
    def binary(self) -> bool:
        return False
