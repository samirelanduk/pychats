import datetime
import os
import pickle
from pychats import Message

def get_conversations(soup, name):
    """Take the soup of the facebook backup and return a list of conversation objects"""

    #Go through the soup and get all the divs which represent a conversation
    conversation_divs = []
    for div in soup.body.contents[1].contents[1:]:
        conversation_divs += div.contents
    print("There are %i conversations here." % len(conversation_divs))

    conversations = [Conversation(x) for x in conversation_divs]

    #Remove user's name from conversations
    for conversation in conversations:
        while name in conversation.members:
            conversation.members.remove(name)

    #Remove conversations with no one else in
    conversations = [x for x in conversations if len(x.members) >= 1]

    return conversations

class Conversation:

    def __init__(self, div):
        #Get a rough idea of the people in this conversation
        self.members = [x for x in div.contents[0].string.split(", ") if "@" not in x]

        #Get the messages
        self.messages = []
        for x in range(int(len(div.contents[1:])/2)):
            self.messages.append(FacebookMessage(div.contents[1:][x*2:(x*2)+2]))

        #Remove all messages by a '@' person
        self.messages = [x for x in self.messages if "@" not in x.sender]

        #Only want messages since January 2011
        self.messages = [x for x in self.messages if x.time > datetime.datetime(2011,1,1)]

        #Put them in the right order
        self.messages.reverse()

        #Add names to members
        for message in self.messages:
            if message.sender not in self.members:
                self.members.append(message.sender)


class FacebookMessage(Message):

    def get_date(self):
        months = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}
        parts = self.facebook_time.split()
        y = int(parts[3])
        m = int(months[parts[2]])
        d = int(parts[1])
        h = int(parts[5].split(":")[0])
        mn = int(parts[5].split(":")[1])
        date = datetime.datetime(y,m,d,h,mn)
        return date

    def __init__(self, divs):
        Message.__init__(self)

        self.text = divs[1].text
        self.sender = divs[0].find(attrs={"class":"user"}).text

        self.facebook_time = divs[0].find(attrs={"class":"meta"}).text
        self.time = self.get_date()

        self.weight = 0 #To be altered later
