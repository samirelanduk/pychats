class Message:

    def __init__(self, text, timestamp, sender):
        self._text = text
        self._timestamp = timestamp
        self._sender = sender


    def __repr__(self):
        return "<Message from %s at %s>" % (
         self._sender.name(),
         self._timestamp.strftime("%Y-%m-%d %H:%M")
        )
