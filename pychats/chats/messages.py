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
