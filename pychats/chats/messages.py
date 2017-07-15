"""This module contains the basic Message class."""

from .people import Contact
from datetime import datetime

class Message:
    """A message sent by someone.

    :param str text: The text of the message.
    :param datetime timestamp: The time the message was sent.
    :param Contact sender: The :py:class:`.Contact` who sent the message."""

    def __init__(self, text, timestamp, sender):
        if not isinstance(text, str):
            raise TypeError("text must be str, not '%s'" % text)
        if not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be datetime, not '%s'" % timestamp)
        if not isinstance(sender, Contact):
            raise TypeError("sender must be Contact object, not '%s'" % sender)
        self._text = text
        self._timestamp = timestamp
        self._sender = sender
        self._conversation = None


    @staticmethod
    def from_json(json):
        """An alternate constructor. It creates a py:class:`.Message` from a
        JSON ``dict``.

        You must also supply an iterable of zero or more py:class:`.Contact`
        objects - if the name of sender in the JSON matches one of these people,
        that object will be set as the sender, and if not a new
        py:class:`.Contact` will be created. Otherwise a new py:class:`.Contact`
        would be created for each message.

        :param dict json: The ``dict`` to convert.
        :param contacts: An iterable of py:class:`.Contact` objects.
        :raises TypeError: if something other than a ``dict`` is given.
        :raises ValueError: if the ``dict`` doesn't have a ``text`` key.
        :raises ValueError: if the ``dict`` doesn't have a ``timestamp`` key.
        :raises ValueError: if the ``dict`` doesn't have a ``sender`` key.
        :raises TypeError: if no py:class:`.Contact` objects are given.
        :rtype: ``Message``"""

        if not isinstance(json, dict):
            raise TypeError("'%s' is not a dict" % str(json))
        if "text" not in json:
            raise ValueError("Message json needs 'text' key: %s" % str(json))
        if "timestamp" not in json:
            raise ValueError("Message json needs 'timestamp' key: %s" % str(json))
        if "sender" not in json:
            raise ValueError("Message json needs 'sender' key: %s" % str(json))
        sender = None
        for person in Contact.all_contacts:
            if person.name() == json["sender"]["name"]:
                sender = person
                break
        else:
            sender = Contact.from_json(json["sender"])
        return Message(
         json["text"],
         datetime.strptime(json["timestamp"], "%Y-%m-%d %H:%M:%S"),
         sender
        )


    def __repr__(self):
        return "<Message from %s at %s>" % (
         self._sender.name(),
         self._timestamp.strftime("%Y-%m-%d %H:%M")
        )


    def text(self, text=None):
        """Returns the text of the message. If a string is provided, the text
        will be updated to that.

        :param str text: If given, the message's text will be updated."""

        if text:
            if not isinstance(text, str):
                raise TypeError("text must be str, not '%s'" % str(text))
            self._text = text
        else:
            return self._text


    def timestamp(self, timestamp=None):
        """Returns the time the message was sent. If a string is provided, the
        timestamp will be updated to that.

        :param datetime timestamp: If given, the message's timestamp will be\
        updated."""

        if timestamp:
            if not isinstance(timestamp, datetime):
                raise TypeError(
                 "timestamp must be datetime, not '%s'" % str(datetime)
                )
            from .conversations import _sort_messages
            self._timestamp = timestamp
            if self._conversation:
                self._conversation._messages = _sort_messages(
                 self._conversation._messages
                )
        else:
            return self._timestamp


    def sender(self, sender=None):
        """Returns the person who sent the message. If a :py:class:`.Contact`
        is provided, the sender will be updated to that.

        :param Contact sender: If given, the message's sender will be updated."""

        if sender:
            if not isinstance(sender, Contact):
                raise TypeError(
                 "sender must be Contact, not '%s'" % str(sender)
                )
            self._sender = sender
        else:
            return self._sender


    def conversation(self):
        """Returns the :py:class:`.Conversation` that the message is part of.
        You cannot set this directly, but it will be updated whenever a message
        is added to a conversation.

        :rtype: ``Conversation``"""

        return self._conversation


    def recipients(self):
        """Returns the :py:class:`.Contact` objects that recieved the message.
        This is determined by the other people in the message's
        :py:class:`.Conversation`.

        :returns: ``set`` of ``Contact``"""

        if self.conversation():
            people = set(self.conversation().participants())
            people.remove(self.sender())
            return people
        else:
            return set()


    def to_json(self):
        """Converts the Message to a JSON dict.

        :rtype: ``dict``"""

        return {
         "text": self._text,
         "timestamp": self._timestamp.strftime("%Y-%m-%d %H:%M:%S"),
         "sender": self._sender.to_json()
        }
