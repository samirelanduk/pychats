from .messages import Message

class Conversation:

    def __init__(self):
        self._messages = []


    def __repr__(self):
        return "<Conversation (%i message%s)>" % (
         len(self._messages), "" if len(self._messages) == 1 else "s"
        )


    def messages(self):
        return list(self._messages)


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
        if not self._messages or message.timestamp() > self._messages[-1].timestamp():
            self._messages.append(message)
        elif message.timestamp() < self._messages[0].timestamp():
            self._messages.insert(0, message)
        else:
            for index, current_message in enumerate(self._messages[:-1]):
                bigger_than_current = message.timestamp() > current_message.timestamp()
                smaller_than_next = message.timestamp() <= self._messages[index + 1].timestamp()
                if bigger_than_current and smaller_than_next:
                    self._messages.insert(index + 1, message)
                    break
        message._conversation = self


    def remove_message(self, message):
        self._messages.remove(message)
