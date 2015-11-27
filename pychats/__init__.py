import datetime

class ChatLog:
    """A collection of contacts and their messages"""

    def __init__(self, contacts):
        self.contacts = sorted(contacts, key=lambda k: k.score)



    def get_contact_by_name(self, name):
        for contact in self.contacts:
            if contact.name == name:
                return contact




class Contact:
    """A person with whom we have spoken"""

    def __init__(self, name, messages):
        self.name = name
        self.messages = sorted(messages, key=lambda k: k.datetime)
        self.start_date = min([m.datetime for m in self.messages])
        self.end_date = max([m.datetime for m in self.messages])
        self.score = sum([m.score for m in self.messages])




class Message:
    """A message, between ourselves and at least one other person."""

    def __init__(self, text, datetime, from_me, weight=1):
        self.text = text
        self.datetime = datetime
        self.from_me = from_me
        self.weight = weight
        self.score = len(self.text) * self.weight



    def __repr__(self):
        return "%s: %s" % (
         datetime.datetime.strftime(self.datetime, "%d-%b-%Y, %H:%M:%S"),
         self.text)
