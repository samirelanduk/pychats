from .messages import Message

class Conversation:

    def __init__(self):
        self._messages = []


    def __repr__(self):
        return "<Conversation (%i messages)>" % len(self._messages)


    def messages(self):
        return self._messages


    def add_message(self, message):
        if not isinstance(message, Message):
            raise TypeError(
             "Can only add Message objects with, not '%s'" % str(message)
            )
        if message in self._messages:
            raise ValueError(
             "Cannot add %s ('%s') to %s as it is already present" % (
              str(message), message.text(), self
             )
            )
        self._messages.append(message)
