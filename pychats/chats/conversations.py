class Conversation:

    def __init__(self):
        self._messages = []


    def __repr__(self):
        return "<Conversation (%i messages)>" % len(self._messages)
