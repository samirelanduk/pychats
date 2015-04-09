from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import datetime
import os

fbIDs = {}

def countMessages(contact):
    num = 0
    for c in contact["conversations"]:
        num += len(c["messages"])
    return num

def makeDate(text):
    months = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}
    parts = text.split()
    y = int(parts[3])
    m = int(months[parts[2]])
    d = int(parts[1])
    h = int(parts[5].split(":")[0])
    mn = int(parts[5].split(":")[1])
    date = datetime.datetime(y,m,d,h,mn)
    return date

def getName(fbID):
    name = ""
    if "@" in fbID:
        #It's an @ address. Has it already been encountered?
        ID = fbID.split("@")[0]
        if ID in fbIDs.keys():
            #Yes it has, assign name
            name = fbIDs[ID]
        else:
            #No it hasn't look it up
            print("Looking up " + fbID)
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
            print("(It was " + name + ")")
        return name
    else:
        return fbID

def processMessageDiv(div):
    conversation = {}
    conversation["members"] = [getName(d) for d in div.contents[0].split(", ")]
    messageDivs = div.contents[1:]
    messages = []
    for x in range(len(messageDivs)//2):
        message = messageDivs[x*2:(x*2)+2]
        messages.append(message)
    messages = [{"text":m[1].text, "sender":getName(m[0].find(attrs={"class":"user"}).text), "fbtime":m[0].find(attrs={"class":"meta"}).text, "time":makeDate(m[0].find(attrs={"class":"meta"}).text)} for m in messages]
    messages.reverse()
    conversation["messages"] = messages
    return conversation

#Get soup of the messages.htm file
print("Starting...")
dirname = "C:\\Users\\Sam\\OneDrive\\7) Computing\\Programming\\Python projects\\5 - Message history\\backups"
f = open(dirname + "/" + [h for h in os.listdir(dirname) if ".htm" in h][0], "rb")
data = f.read()
f.close()
start = datetime.datetime.now()
soup = BeautifulSoup(data)
end = datetime.datetime.now()
print("Soup acquired. It took " + str((end - start).seconds) + " seconds.")

#Get a list of conversations
conversations = []
for div in soup.body.contents[1].contents[1:]:
    conversations += div.contents
print("There are " + str(len(conversations)) + " conversations here.")

#Get a list of conversation members
members = [c.contents[0].split(", ") for c in conversations]
oneperson = [m for m in members if len(m) == 1]
twopeople = [m for m in members if len(m) == 2]
multiperson = [m for m in members if len(m) > 2]

#Get everything in the right category
for members in twopeople:
    if "Sam Ireland" in members:
        members.remove("Sam Ireland")
    elif "1359142679@facebook.com" in members:
        members.remove("1359142679@facebook.com")
    else:
        #This conversation has two people in it but neither are me - it belongs in the group chat list
        multiperson.append(members)
        members.append("_0_")
twopeople = [t for t in twopeople if "_0_" not in t]
twopeople += [o for o in oneperson if "Sam Ireland" not in o and "1359142679@facebook.com" not in o]
twopeople = [t[0] for t in twopeople]

print(str(len(twopeople)) + " have two people in them.")
print(str(len(multiperson)) + " have more than two people in them.")

#Define contacts as all the people I've had a private conversation with. Therefore, if someone has
#communicated with me only in group chat, they are ignored.
contacts = list(set([getName(t) for t in twopeople]))
print("There are " + str(len(contacts)) + " contacts.")
        
#Give each contact their own message divs
contacts = [{"name":c,"conversations":[]} for c in contacts if c != "Sam Ireland"]
for contact in contacts:
    for conv in conversations:
        people = conv.contents[0].split(", ")
        if contact["name"] in people:
            contact["conversations"].append(conv)

#Make these divs a bit more readable
for c in contacts:
    c["conversations"] = [processMessageDiv(div) for div in c["conversations"]]

#Remove my name from the conversations
for c in contacts:
    for conv in c["conversations"]:
        if "Sam Ireland" in conv["members"]:
            conv["members"].remove("Sam Ireland")
        elif "1359142679@facebook.com" in conv["members"]:
            conv["members"].remove("1359142679@facebook.com")

#Sort conversations by number of messages in them
for c in contacts:
    c["conversations"] = sorted(c["conversations"], key=lambda k: len(k["messages"]))
    c["conversations"].reverse()

#Remove empty conversation contacts etc
contacts = [c for c in contacts if len(c["conversations"]) != 0 and "@" not in c["name"] and countMessages(c) > 1]

#Finally, give each contact a combined list of messages, weighted according to group size
for c in contacts:
    c["combinedMessages"] = []
    for conv in c["conversations"]:
        for m in conv["messages"]:
            weight = 0
            if m["sender"] == "Sam Ireland" or m["sender"] == c["name"]:
                weight = 1/len(conv["members"])
            message = m
            message.update({"weight":weight})
            c["combinedMessages"].append(message)
    c["combinedMessages"] = sorted(c["combinedMessages"], key=lambda k:k["time"])
    c["combinedMessages"] = [c for c in c["combinedMessages"] if c["text"] != ""]
    c["num"] = 0
    for cm in c["combinedMessages"]:
        c["num"] += cm["weight"]

contacts = sorted(contacts, key=lambda k: k["num"])
contacts.reverse()

