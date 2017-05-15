"""This module contains the Contact class used to represent people."""

class Contact:
    """A person who has sent at least one message.

    :param str name: The person's name."""

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be str, not '%s'" % name)
        self._name = name
        self._tags = set()


    def __repr__(self):
        return "<Contact: %s>" % self._name


    def name(self, name=None):
        """Returns the contact's name. If a string is provided, the name will be
        updated to that.

        :param str name: If given, the contact's name will be updated."""

        if name:
            if not isinstance(name, str):
                raise TypeError("name must be str, not '%s'" % name)
            self._name = name
        else:
            return self._name


    def tags(self):
        """Returns any tags associated with the contact. These can be used to
        categorise different contacts, such as by gender or group of friends.

        :rtype: ``set``"""

        return set(self._tags)


    def add_tag(self, tag):
        """Adds a tag to the Contact.

        :param str tag: The tag to add.
        :raises TypeError: if the tag given is not a string."""

        if not isinstance(tag, str):
            raise TypeError("tag must be str, not '%s'" % tag)
        self._tags.add(tag)


    def remove_tag(self, tag):
        """Removes a tag from the Contact.

        :param str tag: The tag to remove."""

        self._tags.remove(tag)
