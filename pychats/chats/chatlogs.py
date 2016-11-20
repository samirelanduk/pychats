from .conversations import Conversation

class ChatLog:

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be str, not '%s'" % name)
        self._name = name
        self._conversations = set()


    def __repr__(self):
        return "<'%s' ChatLog (%i Conversations)>" % (
         self._name, len(self._conversations)
        )


    def name(self, name=None):
        if name:
            if not isinstance(name, str):
                raise TypeError("name must be str, not '%s'" % name)
            self._name = name
        else:
            return self._name


    def conversations(self):
        return set(self._conversations)


    def add_conversation(self, conversation):
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
