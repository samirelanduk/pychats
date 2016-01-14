import datetime
from .markov import *
from .htmlgen import *
from .charts import *

class ChatLog(ChartGeneratingLog):
    """A collection of contacts and their messages"""

    def __init__(self, contacts, my_name):
        self.contacts = sorted(contacts, key=lambda k: k.score, reverse=True)
        self.my_name = my_name
        self.messages = []
        for contact in self.contacts:
            self.messages += contact.messages
            contact.log = self
        self.messages = sorted(self.messages, key=lambda k: k.datetime)
        self.start_date =  min([c.start_date for c in self.contacts])
        self.end_date = max([c.end_date for c in self.contacts])



    def get_contact_by_name(self, name):
        for contact in self.contacts:
            if contact.name == name:
                return contact




class Contact(MarkovGenerator, HtmlGeneratingContact, ChartGeneratingContact):
    """A person with whom we have spoken"""

    def __init__(self, name, messages):
        MarkovGenerator.__init__(self, messages)
        self.name = name
        self.messages = sorted(messages, key=lambda k: k.datetime)
        for message in self.messages:
            message.contact = self
        self.start_date = min([m.datetime for m in self.messages])
        self.end_date = max([m.datetime for m in self.messages])
        self.score = sum([m.score for m in self.messages])




class Message(MarkovEntity, HtmlGeneratingMessage):
    """A message, between ourselves and at least one other person.

    A message only makes sense in the context of its owner - an identical message
    might appear in two contacts, with different weights in each."""

    name = "Generic"
    color = "#777777"

    def __init__(self, text, datetime, from_me, from_them, sender_name=None, weight=1):
        MarkovEntity.__init__(self, text, from_them)
        self.text = text
        self.datetime = datetime
        self.from_me = from_me
        self.from_them = from_them
        self.weight = weight
        self.score = len(self.text) * self.weight

        #If this is from someone other than us or the contact - there MUST be a
        #name. If it is from us or the contact, sender_name will be None regardless
        #of what is passed
        if not from_me and not from_them:
            if sender_name:
                self.sender_name = sender_name
            else:
                raise Exception(
                 "Cannot create a message that is not from us or them, and has no name given."
                )
        else:
            self.sender_name = None #Even if a sender_name argument is given


    def __repr__(self):
        return "%s: %s" % (
         datetime.datetime.strftime(self.datetime, "%d-%b-%Y, %H:%M:%S"),
         self.text)
