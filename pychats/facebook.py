import datetime
import os
import requests
import pickle

fbIDs = {}
if "fbIDs.p" in os.listdir("."):
    f = open("fbIDs.p", "rb")
    fbIDs = pickle.load(f)
    f.close()

def get_facebook_name(fbID):
    name = ""
    if False:#"@" in fbID:
        #It's an @ address. Has it already been encountered?
        ID = fbID.split("@")[0]
        if ID in fbIDs.keys():
            #Yes it has, assign name
            name = fbIDs[ID]
        else:
            #No it hasn't look it up
            #print("Looking up " + fbID)
            print("Sending a request for " + fbID + "...")
            text = str(requests.get("http://graph.facebook.com/" + ID).text)
            pairs = text[1:-1].split(",")
            obj = {}
            for p in pairs:
                obj[p.split(":")[0][1:-1]] = p.split(":")[1][1:-1]
            if "first_name" in obj.keys() and "last_name" in obj.keys():
                name = obj["first_name"] + " " + obj["last_name"]
                fbIDs[ID] = name
            else:
                name = fbID
            #print("(It was " + name + ")")
        return name
    else:
        #This is already a facebook name
        return fbID

def get_conversations(soup, name):
    """Take the soup of the facebook backup and return a list of conversation objects"""

    #Go through the soup and get all the divs which represent a conversation
    conversation_divs = []
    for div in soup.body.contents[1].contents[1:]:
        conversation_divs += div.contents
    print("There are %i conversations here." % len(conversation_divs))

    conversations = [Conversation(x) for x in conversation_divs]

    #Update the locally stored fbIDs
    f = open("fbIDs.p", "wb")
    pickle.dump(fbIDs, f)
    f.close()

    #Remove user's name from conversations
    for conversation in conversations:
        while name in conversation.members:
            conversation.members.remove(name)

    #Remove conversations with no one else in
    conversations = [x for x in conversations if len(x.members) >= 1]

    return conversations

class Conversation:

    def __init__(self, div):
        self.members = [get_facebook_name(x) for x in div.contents[0].string.split(", ") if "@" not in x]

        #Get the messages
        self.messages = []
        for x in range(int(len(div.contents[1:])/2)):
            self.messages.append(FacebookMessage(div.contents[1:][x*2:(x*2)+2]))

        #Only want messages since January 2011
        self.messages = [x for x in self.messages if x.time > datetime.datetime(2011,1,1)]
        
        #Add names to members
        for message in self.messages:
            if message.sender not in self.members:
                self.members.append(message.sender)

class FacebookMessage:

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
        self.text = divs[1].text
        self.sender = get_facebook_name(divs[0].find(attrs={"class":"user"}).text)

        self.facebook_time = divs[0].find(attrs={"class":"meta"}).text
        self.time = self.get_date()
