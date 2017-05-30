"""This module handles the conversion of Message objects to JSON and back."""

from ..chats.messages import Message
from .contact_json import contact_to_json

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
