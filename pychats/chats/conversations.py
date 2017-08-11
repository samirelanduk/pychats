"""This module contains the Conversation class."""

from .messages import Message

class Conversation:
    """Represents a conversation between two or more people. Ultimately it is a
    collection of messages, each of which has a sender."""

    def __init__(self):
        self._messages = []
        self._chatlog = None


    def __len__(self):
        return self.length()


    @staticmethod
    def from_json(json):
        """An alternate constructor. It creates a py:class:`.Conversation` from
        a JSON ``dict``.

        :param dict json: The ``dict`` to convert.
        :raises TypeError: if something other than a ``dict`` is given.
        :raises ValueError: if the ``dict`` doesn't have a ``messages`` key.
        :rtype: ``Conversation``"""

        if not isinstance(json, dict):
            raise TypeError("'%s' is not a dict" % str(json))
        if "messages" not in json:
            raise ValueError("Conversation json needs 'messages' key: %s" % str(json))
        messages = [Message.from_json(m) for m in json["messages"]]
        messages = _sort_messages(messages)
        conversation = Conversation()
        conversation._messages = messages
        return conversation


    def __repr__(self):
        return "<Conversation (%i message%s)>" % (
         len(self._messages), "" if len(self._messages) == 1 else "s"
        )


    def messages(self):
        """Returns the :py:class:`.Message` objects in the conversation.

        :rtype: ``Message``"""

        return list(self._messages)


    def add_message(self, message):
        """Adds a :py:class:`.Message` to the conversation.

        You cannot add a message if it is already in the conversation, and
        regardless of the order in which you add messages, they will be stored
        in order of the messages' timestamps.

        :param Message message: the ``Message`` to remove.
        :raises ValueError: if a message is given that is already there."""

        if not isinstance(message, Message):
            raise TypeError("'%s' is not a Message object" % str(message))
        if message in self._messages:
            raise ValueError(
             "'%s' is already in '%s'" % (str(message), str(self))
            )
        if self._messages and message.timestamp() < self._messages[0].timestamp():
            self._messages.insert(0, message)
        else:
            self._messages.append(message)
            if len(self._messages) > 1\
             and message.timestamp() < self._messages[-2].timestamp():
                self._messages = sorted(self._messages, key=lambda k: k.timestamp())
        message._conversation = self


    def remove_message(self, message):
        """Removes a :py:class:`.Message` from the conversation.

        :param Message message: the ``Message`` to remove."""

        self._messages.remove(message)
        message._conversation = None


    def length(self):
        """Returns the number of messages in the conversation.

        :rtype: ``int``"""

        return len(self._messages)


    def chatlog(self):
        """Returns the :py:class:`.ChatLog` the conversation is a part of.You
        cannot set this directly, but it will be updated whenever a conversation
        is added to a chatlog.

        :rtype: ``Chatlog``"""

        return self._chatlog


    def participants(self):
        """Returns all the :py:class:`.Contact` objects who have sent messages
        in this conversation."""

        participants = set()
        for message in self.messages():
            participants.add(message.sender())
        return participants


    def to_json(self):
        """Converts the Conversation to a JSON dict.

        :rtype: ``dict``"""

        return {"messages": [message.to_json() for message in self._messages]}



def _sort_messages(messages):
    return sorted(messages, key=lambda k: k.timestamp())
