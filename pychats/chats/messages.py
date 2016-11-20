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
        self._conversation = None


    def __repr__(self):
        return "<Message from %s at %s>" % (
         self._sender.name(),
         self._timestamp.strftime("%Y-%m-%d %H:%M")
        )


    def text(self, text=None):
        if text:
            if not isinstance(text, str):
                raise TypeError("text must be str, not '%s'" % str(text))
            self._text = text
        else:
            return self._text


    def timestamp(self, timestamp=None):
        if timestamp:
            if not isinstance(timestamp, datetime):
                raise TypeError(
                 "timestamp must be datetime, not '%s'" % str(datetime)
                )
            self._timestamp = timestamp
            if self.conversation():
                conversation = self.conversation()
                conversation.remove_message(self)
                conversation.add_message(self)
        else:
            return self._timestamp


    def sender(self, sender=None):
        if sender:
            if not isinstance(sender, Contact):
                raise TypeError(
                 "sender must be Contact, not '%s'" % str(sender)
                )
            self._sender = sender
        else:
            return self._sender


    def conversation(self):
        return self._conversation
