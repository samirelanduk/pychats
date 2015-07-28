import datetime

def facebook_backup(file, my_name=""):
    from . import facebook
    from bs4 import BeautifulSoup

    #Need to know user's Facebook name
    if my_name == "":
        my_name = input("What is your Facebook name? ")

    #Open the file to get the html
    html = file.read()
    print("Getting soup (can take a few seconds)...")
    soup = BeautifulSoup(html)

    #Get conversations
    conversations = facebook.get_conversations(soup, my_name)
    conversations = [x for x in conversations if len(x.messages) >= 4]

    #Divide into direct and group conversations
    directs = [x for x in conversations if len(x.members) == 1]
    groups = [x for x in conversations if len(x.members) > 1]

    #Define contacts as those with whom the user has spoken to directly
    contacts = list(set([conv.members[0] for conv in directs]))
    contacts = [Contact(x) for x in contacts]
    print("There are %i contacts here." % len(contacts))
    #Create a backup object to contain the contacts
    backup = Backup(contacts)

    #Give each contact their direct messages
    for conv in directs:
        person = backup.get_contact_by_name(conv.members[0])
        person.messages += conv.messages

    #Assign a weight of 1 to all messages currently in the backup
    for person in contacts:
        for message in person.messages:
            message.weight = 1

    #

    #Sort everything
    backup.sort_contacts()

    return backup

class Backup:

    def __init__(self, contacts):
        self.contacts = contacts
        self.start_date = None
        self.end_date = None

    def get_contact_by_name(self, name):
        for contact in self.contacts:
            if contact.name == name:
                return contact

    def set_range(self):
        """Assigns values to start_date and end_date according to current contacts.
        Requires contacts to have these set."""
        self.start_date = min([x.start_date for x in self.contacts])
        self.end_date = max([x.start_date for x in self.contacts])

    def sort_contacts(self):
        #Put all contact messages in correct order
        for contact in self.contacts:
            contact.sort_messages()

        #Sort contacts by number of chars
        self.contacts = sorted(self.contacts, key = lambda k: k.chars)
        self.contacts.reverse()

        self.set_range()

class Contact:

    def __init__(self, name):
        self.name = name
        self.messages = []
        self.start_date = None
        self.end_date = None
        self.chars = 0

    def sort_messages(self):
        #Get messages in right order
        self.messages = sorted(self.messages, key = lambda k: k.time)

        #Update contact start and end dates
        self.start_date = self.messages[0].time
        self.end_date = self.messages[-1].time

        self.chars = sum([len(x.text) for x in self.messages])
