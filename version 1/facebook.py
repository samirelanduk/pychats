from bs4 import BeautifulSoup
import requests
import datetime
import os
import calendar
import sms

fbIDs = {}
#Get the real name (takes a while...)
def getRealName(fbID):
    name = ""
    if "@" in fbID:
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
        return fbID
    

#This takes a facebook date string and returns a normal datetime object
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

#This function takes a message div and returns a neat message dictionary
def processMessage(mess_div):
    message = {}
    message["text"] = mess_div[1].text
    message["sender"] = getRealName(mess_div[0].find(attrs={"class":"user"}).text)
    message["from_me"] = False
    if message["sender"] == "Sam Ireland":
        message["from_me"] = True
    message["fbtime"] = mess_div[0].find(attrs={"class":"meta"}).text
    message["time"] = makeDate(mess_div[0].find(attrs={"class":"meta"}).text)
    message["type"] = "facebook"
    message["group"] = False    #for now
    return message
    
        

#This function takes a conversation div and returns a neat conversation dictionary
def processConversation(con_div):
    conversation = {}
    #Get the members, as displayed in the html
    conversation["members"] = [getRealName(n) for n in con_div.contents[0].string.split(", ")]

    #Get the messages
    conversation["messages"] = []
    for x in range(int(len(con_div.contents[1:])/2)):
        message = con_div.contents[1:][x*2:(x*2)+2]
        conversation["messages"].append(message)
    conversation["messages"] = [processMessage(m) for m in conversation["messages"]]
    conversation["messages"].reverse()

    #Add members not shown but who appear in messages
    for message in conversation["messages"]:
        if message["sender"] not in conversation["members"]:
            conversation["members"].append(message["sender"])

    #Remove any member who is 'Sam Ireland'
    conversation["members"] = [c for c in conversation["members"] if c != "Sam Ireland" and "@" not in c]
    return conversation


#This function takes the messages html file and gets a list of conversations from it
def getConversations(html):
    #Get soup of page
    f = open(html, "rb")
    data = f.read()
    f.close()

    print("Getting soup...")
    start = datetime.datetime.now()
    soup = BeautifulSoup(data)
    end = datetime.datetime.now()
    print("Soup acquired. It took " + str((end - start).seconds) + " seconds.")

    #Get a list of conversation divs
    conversation_divs = []
    for div in soup.body.contents[1].contents[1:]:
        conversation_divs += div.contents
    print("There are " + str(len(conversation_divs)) + " conversations here.")

    #Clean up and return
    print("Processing conversations...")
    conversations = [processConversation(c) for c in conversation_divs]

    return conversations

#Returns a list of contacts with messages attached
def get_all_facebook(directory):
    #Get a list of conversations
    html = directory + "//" + [f for f in os.listdir(directory) if f == "messages.htm"][0]
    conversations = getConversations(html)

    #Get all the one-on-one conversations
    directs = []
    for conv in conversations:
        if len(conv["members"]) <= 1:
            conv["assigned"] = True
            directs.append(conv)
        else:
            conv["assigned"] = False
    directs = [d for d in directs if len(d["members"]) > 0]
    print(str(len([c for c in conversations if c["assigned"]])) + " of these are direct conversations")
    print(str(len([c for c in conversations if not c["assigned"]])) + " group conversations remain")

    #Define contacts as all people I've had a direct conversation with
    contacts = []
    for d in directs:
        contacts.append(d["members"][0])
    contacts = list(set(contacts))
    contacts = [{"name":c, "messages":[], "message_count":0, "message_length_count":0} for c in contacts]
    print("After merging, there are " + str(len(contacts)) + " contacts.")

    #Give each contact their direct messages
    for c in contacts:
        for d in directs:
            if c["name"] == d["members"][0]:
                c["messages"] += d["messages"]
        for m in c["messages"]:
            m.update({"weight":1})

    #Now give them all their group messages
    groups = [g for g in conversations if not g["assigned"]]
    for c in contacts:
        for g in groups:
            if c["name"] in g["members"]:
                for message in g["messages"]:
                    m = dict(message)
                    m.update({"weight":0})
                    m["group"] = True
                    if m["sender"] == "Sam Ireland" or m["sender"] == c["name"]:
                        m["weight"] = 1/(len(g["members"])-1)
                    c["messages"].append(m)

    #Sort and prep contacts, then return them
    contacts = [c for c in contacts if len(c["messages"]) > 1 and "@" not in c["name"] and "Sam Ireland" in [m["sender"] for m in c["messages"]]]
    sms.deduplicate(contacts)
    for person in contacts:
        sms.sortMessages(person)
        for message in person["messages"]:
            person["message_count"] += message["weight"]
            person["message_length_count"] += (len(message["text"]) * message["weight"])

    contacts = sorted(contacts, key=lambda k: k["message_length_count"], reverse=True)

    return contacts

def findString(s, contacts):
    for p in contacts:
        if s in "".join(p["members"]): print(p["members"])

if __name__ == "__main__":
    import pickle
    location = input("Where is the backup loacated? ")
    file_name = input("What shall the dump be called? ")
    if file_name[-2:] == ".p": file_name = file_name[:-2]
    print("")
    
    data = get_all_facebook(location)

    f = open(location + "\\" + file_name + ".p", "wb")
    pickle.dump(data, f)
    
