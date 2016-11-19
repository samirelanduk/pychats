from .people import Contact
from datetime import datetime

class Message:

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


    def __repr__(self):
        return "<Message from %s at %s>" % (
         self._sender.name(),
         self._timestamp.strftime("%Y-%m-%d %H:%M")
        )


    def text(self):
        return self._text


    def timestamp(self):
        return self._timestamp


    def sender(self):
        return self._sender
