"""This module handles the conversion of Message objects to JSON and back."""

from datetime import datetime
from ..chats.messages import Message
from ..chats.people import Contact
from .contact_json import contact_to_json, json_to_contact

def message_to_json(message):
    """Takes a :py:class:`.Message` and converts it to a JSON dict.

    :param Message message: the message object to convert.
    :raises TypeError: if something other than a py:class:`.Message` is given.
    :rtype: ``dict``"""

    if not isinstance(message, Message):
        raise TypeError("'%s' is not a Message object" % str(message))
    return {
     "text": message.text(),
     "timestamp": message.timestamp().strftime("%Y-%m-%d %H:%M:%S"),
     "sender": contact_to_json(message.sender())
    }


def json_to_message(json, contacts):
    """Creates a py:class:`.Message` from a JSON ``dict``.

    You must also supply an iterable of zero or more py:class:`.Contact`
    objects - if the name of sender in the JSON matches one of these people,
    that object will be set as the sender. Otherwise a new py:class:`.Contact`
    will be created. Otherwise a new py:class:`.Contact` would be created for
    each message.

    :param dict json: The ``dict`` to convert.
    :param contacts: An iterable of py:class:`.Contact` objects.
    :raises TypeError: if something other than a ``dict`` is given.
    :raises ValueError: if the ``dict`` doesn't have a ``text`` key.
    :raises ValueError: if the ``dict`` doesn't have a ``timestamp`` key.
    :raises ValueError: if the ``dict`` doesn't have a ``sender`` key.
    :raises TypeError: if none py:class:`.Contact` objects are given.
    :rtype: ``Message``"""
    
    if not isinstance(json, dict):
        raise TypeError("'%s' is not a dict" % str(json))
    if "text" not in json:
        raise ValueError("Message json must have 'text' key: %s" % str(json))
    if "timestamp" not in json:
        raise ValueError("Message json must have 'timestamp' key: %s" % str(json))
    if "sender" not in json:
        raise ValueError("Message json must have 'sender' key: %s" % str(json))
    for contact in contacts:
        if not isinstance(contact, Contact):
            raise TypeError("'%s' is not a Contact" % str(contact))
    sender = None
    for person in contacts:
        if person.name() == json["sender"]["name"]:
            sender = person
            break
    else:
        sender = json_to_contact(json["sender"])
    return Message(
     json["text"],
     datetime.strptime(json["timestamp"], "%Y-%m-%d %H:%M:%S"),
     sender
    )
