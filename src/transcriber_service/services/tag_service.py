from ..domain import Tag, RecordTag, TagException


class TagService(object):
    """
    Manages tagging operations and relationships between tags and audio records.

    Provides functionality to associate/dissociate tags with records, search records by tags,
    and maintain tag consistency across the system.
    """

    def __init__(self):
        """Initializes a new TagService with empty tag and record-tag collections."""

        self.__tags: list[Tag] = []
        self.__record_tags: list[RecordTag] = []

    def add_tag_to_record(self, tag_name: str, record_id: str) -> None:
        """
        Associates a tag with an audio record.

        Note: if tag does not exist, it will be created.

        :param tag_name: Name of the tag to associate.
        :param record_id: ID of the audio record to associate.
        :raises TagException: If the tag already exists for this record.
        """

        tag_id = self._find_tag_id(tag_name)

        if tag_id is not None:
            if self._find_tag_record(tag_id, record_id):
                raise TagException('Tag already exists.')
        else:
            tag_id = self._create_tag_id(tag_name)

        self.__record_tags.append(RecordTag(tag_id, record_id))

    def remove_tag_from_record(self, tag_name: str, record_id: str) -> None:
        """
        Removes a tag association from an audio record.

        :param tag_name: Name of the tag to remove.
        :param record_id: ID of the audio record.
        :raises TagException: If tag or association doesn't exist.
        """

        tag_id = self._find_tag_id(tag_name)
        if not tag_id:
            raise TagException('Tag not found.')

        record_tag = self._find_tag_record(tag_id, record_id)
        if not record_tag:
            raise TagException('There is no audio record with that tag.')

        self.__record_tags.remove(record_tag)

    def find_records_by_tag(self, tag_name: str) -> tuple:
        """
        Finds all records associated with a specific tag.

        :param tag_name: Name of the tag to search for.
        :return: A tuple of the record IDs associated with the tag.
        :raises TagException: If the tag does not exist.
        """

        tag_id = self._find_tag_id(tag_name)
        if not tag_id:
            raise TagException('Tag not found.')

        return tuple(self._find_records(tag_id))

    def find_tags_by_record(self, record_id: str) -> tuple:
        """
        Retrieves all tags associated with a specific record.

        :param record_id: ID of the record to search for.
        :return: A tuple of the tag IDs associated with the record.
        """

        return tuple(record_tag.tag_id for record_tag in self.__record_tags if record_tag.record_id == record_id)

    def _find_tag_id(self, tag_name: str) -> str | None:
        """Finds tag ID by name (case-insensitive search)."""
        for tag in self.__tags:
            if tag.name == tag_name.lower():
                return tag.id

    def _find_records(self, tag_id: str):
        """Generator yielding record IDs associated with a tag ID."""
        return (record_tag.record_id for record_tag in self.__record_tags if record_tag.tag_id == tag_id)

    def _create_tag_id(self, tag_name: str) -> str:
        """Creates new tag and returns its ID."""
        self.__tags.append(Tag(tag_name.lower()))
        return self.__tags[-1].id

    def _find_tag_record(self, tag_id: str, record_id) -> RecordTag | None:
        """Finds specific tag-record association."""
        for record_tag in self.__record_tags:
            if record_tag.tag_id == tag_id and record_tag.record_id == record_id:
                return record_tag
