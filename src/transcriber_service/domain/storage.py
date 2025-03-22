from uuid import uuid4


class Storage(object):
    def __init__(self, user_id: str):
        """
        Represents a user's personal storage container for audio records.

        :param user_id: The user's ID (only one user for storage).
        """

        self.__id = uuid4().hex
        self.__user_id = user_id
        self.__audio_record_ids: list[str] = []

    @property
    def id(self) -> str:
        """Return ID of the storage container."""
        return self.__id

    @property
    def user_id(self) -> str:
        """Return the ID of owner user."""
        return self.__user_id

    @property
    def audio_record_ids(self) -> list[str]:
        """Return a list of audio record IDs."""
        return self.__audio_record_ids.copy()

    def add_audio_record(self, record_id: str) -> None:
        """
        Add audio record to storage.

        :param record_id: The audio record ID to add.
        :return: None
        """
        if record_id not in self.__audio_record_ids:
            self.__audio_record_ids.append(record_id)

    def remove_audio_record(self, record_id: str) -> None:
        """
        Remove audio record from storage.

        :param record_id: The audio record ID to remove.
        :return: None
        """
        self.__audio_record_ids.remove(record_id)
