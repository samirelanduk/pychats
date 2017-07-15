"""This module contains the Contact class used to represent people."""

import weakref

class Contact:
    """A person who has sent at least one message.

    :param str name: The person's name."""

    all_contacts = set()

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be str, not '%s'" % name)
        self._name = name
        self._tags = set()
        Contact.all_contacts.add(self)


    @staticmethod
    def from_json(json):
        """An alternate constructor. It creates a py:class:`.Contact` from a
        JSON ``dict``.

        :param dict json: The ``dict`` to convert.
        :raises TypeError: if something other than a ``dict`` is given.
        :raises ValueError: if the ``dict`` doesn't have a ``name`` key.
        :raises ValueError: if the ``dict`` doesn't have a ``tags`` key.
        :rtype: ``Contact``"""

        if not isinstance(json, dict):
            raise TypeError("'%s' is not a dict" % str(json))
        if "name" not in json:
            raise ValueError("Contact json must have 'name' key: %s" % str(json))
        if "tags" not in json:
            raise ValueError("Contact json must have 'tags' key: %s" % str(json))
        contact = Contact(json["name"])
        for tag in json["tags"]:
            contact.add_tag(tag)
        return contact


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


    def to_json(self):
        """Converts the Contact to a JSON dict.

        :rtype: ``dict``"""

        return {
         "name": self.name(),
         "tags": sorted(list(self._tags))
        }
