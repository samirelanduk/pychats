"""This module handles the conversion of Contact objects to JSON and back."""

from ..chats.people import Contact

def contact_to_json(contact):
    """Takes a :py:class:`Contact` and converts it to a JSON dict.

    :param Contact contact: the contact object to convert.
    :rtype: ``dict``"""

    if not isinstance(contact, Contact):
        raise TypeError("'%s' is not a Contact object" % str(contact))
    return {"name": contact.name()}
