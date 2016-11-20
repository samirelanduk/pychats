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
