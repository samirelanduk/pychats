"""This module contains the Chatlog class."""

from .conversations import Conversation

class ChatLog:
    """A collection of :py:class:`.Conversation` objects from a single source.

    :param str name: The name of the chatlog."""

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be str, not '%s'" % name)
        self._name = name
        self._conversations = set()


    def __repr__(self):
        return "<'%s' ChatLog (%i Conversation%s)>" % (
         self._name,
         len(self._conversations),
         "" if len(self._conversations) == 1 else "s"
        )


    def name(self, name=None):
        """Returns the name of the chatlog. If a string is provided, the
        name will be updated to that.

        :param str name: If given, the chatlog's name will be updated."""

        if name:
            if not isinstance(name, str):
                raise TypeError("name must be str, not '%s'" % name)
            self._name = name
        else:
            return self._name


    def conversations(self):
        """Returns all the :py:class:`.Conversation` objects in this chatlog.

        :returns: ``set`` of ``Conversation``"""

        return set(self._conversations)


    def add_conversation(self, conversation):
        """Adds a :py:class:`.Conversation` to the chatlog. You can only add a
        conversation if it is not already in the chatlog.

        :param Conversation conversation: the conversation to add.
        :raises ValueError: if you try to add a conversation that is already\
        there."""

        if not isinstance(conversation, Conversation):
            raise TypeError(
             "Can only add Conversation objects, not '%s'" % conversation
            )
        if conversation in self._conversations:
            raise ValueError(
             "Cannot add %s to %s as it is already present" % (
              str(conversation), self
             )
            )
        self._conversations.add(conversation)
        conversation._chatlog = self


    def remove_conversation(self, conversation):
        """Removes a :py:class:`.Conversation` to the chatlog.

        :param Conversation conversation: the conversation to remove."""

        self._conversations.remove(conversation)
