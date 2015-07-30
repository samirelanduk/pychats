import copy
import random

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

    #Give each contact their group messages
    for person in contacts:
        for conv in groups:
            if person.name in conv.members:
                for message in conv.messages:
                    new_message = copy.deepcopy(message)
                    if new_message.sender == my_name or new_message.sender == person.name:
                        new_message.weight = 1.0 / len(conv.members)
                    else:
                        new_message.weight = 0
                    person.messages.append(new_message)

    #Sort everything
    backup.sort_contacts()

    #Make Markov-ready
    backup.prime_for_markov()

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

        #Sort contacts by score
        self.contacts = sorted(self.contacts, key = lambda k: k.score)
        self.contacts.reverse()

        #Assign the start and end points of the backup
        self.set_range()

    def prime_for_markov(self):

        #Make all contacts make themselves Markov-ready
        for contact in self.contacts:
            contact.prime_for_markov()

class Contact:

    def __init__(self, name):
        self.name = name
        self.messages = []
        self.start_date = None
        self.end_date = None
        self.score = 0
        self.initial_distribution = []

    def sort_messages(self):
        #Get messages in right order
        self.messages = sorted(self.messages, key = lambda k: k.time)

        #Update contact start and end dates
        self.start_date = self.messages[0].time
        self.end_date = self.messages[-1].time

        self.score = sum([len(x.text) * x.weight for x in self.messages])

    def prime_for_markov(self):
        for message in self.messages:
            message.set_markov_words()

        self.initial_distribution = [x.markov_words[0] for x in self.messages if len(x.markov_words) > 1 and x.sender == self.name]

    def get_first_word(self):
        if len(self.initial_distribution) != 0:
            return random.choice(self.initial_distribution)

    def get_next_word(self, current_word):
        possibles = []
        for message in self.messages:
            if current_word in message.markov_words:
                x = 0
                for word in message.markov_words:
                    if word == current_word:
                        possibles.append(message.markov_words[x+1])
                    x += 1
        return random.choice(possibles)

    def generate_message(self):
        message = []
        message.append(self.get_first_word())

        while message[-1] != None:
            message.append(self.get_next_word(message[-1]))

        return " ".join(message[:-1])


class Message:

    def __init__(self):
        self.markov_words = []

    def set_markov_words(self):
        #This will do for now
        self.markov_words = self.text.split(" ") + [None]
