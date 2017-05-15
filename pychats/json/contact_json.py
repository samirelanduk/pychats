"""This module handles the conversion of Contact objects to JSON and back."""

from ..chats.people import Contact

def contact_to_json(contact):
    """Takes a :py:class:`.Contact` and converts it to a JSON dict.

    :param Contact contact: the contact object to convert.
    :raises TypeError: if something other than a py:class:`.Contact` is given.
    :rtype: ``dict``"""

    if not isinstance(contact, Contact):
        raise TypeError("'%s' is not a Contact object" % str(contact))
    return {
     "name": contact.name(),
     "tags": sorted(list(contact.tags()))
    }


def json_to_contact(json):
    """Creates a py:class:`.Contact` from a JSON ``dict``.

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
    contact._tags = set(json["tags"])
    return contact
