from uuid import uuid4


class Storage:
    def __init__(self, user_id: str):
        """
        Represents a user's personal storage container for audio records.

        :param user_id: The user's ID (only one user for storage).
        """

        self.__id = uuid4().hex
        self.__user_id = user_id

    @property
    def id(self) -> str:
        return self.__id

    @property
    def user_id(self) -> str:
        return self.__user_id
