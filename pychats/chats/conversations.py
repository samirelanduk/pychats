class Conversation:

    def __init__(self):
        self._messages = []


    def __repr__(self):
        return "<Conversation (%i messages)>" % len(self._messages)


    def add_message(self, message):
        self._messages.append(message)
