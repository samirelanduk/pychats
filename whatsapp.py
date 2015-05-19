import sqlite3
import datetime
import os
import sms

#I'll fix this later...
my_number = input("What is your phone number? (format +xx0000...) ")

#This function takes the mangled whatsapp ID and returns a formatted phone number
def processNumber(whatsappID):
    number = whatsappID
    if number is None: number = ""
    if "@" in number: number = number.split("@")[0]
    if "-" in number: number = number.split("-")[0]
    if number.isnumeric(): number = "+" + number
    return number

#This funtction takes a row from message table and returns a cleaned up dictionary
def processMessage(zwamessage_row):
    message = {}
    message["text"] = zwamessage_row["ZTEXT"]
    message["time"] = datetime.datetime.utcfromtimestamp(zwamessage_row["ZMESSAGEDATE"]+978264000)
    message["from_me"] = bool(zwamessage_row["ZISFROMME"])
    message["chat_session"] = zwamessage_row["ZCHATSESSION"]
    if message["from_me"]:
        message["sender"] = my_number
    else:
        message["sender"] = processNumber(zwamessage_row["ZFROMJID"])
    message["receiver"] = processNumber(zwamessage_row["ZTOJID"])
    message["message_type"] = zwamessage_row["ZMESSAGETYPE"]
    message["group_member"] = zwamessage_row["ZGROUPMEMBER"]
    if message["message_type"] > 0 and message["message_type"] < 6:
        message["text"] = "<<MEDIA>>"
    message["media"] = zwamessage_row["ZMEDIAITEM"]
    message["type"] = "whatsapp"
    message["group"] = False
    return message


#Cleans up chatsession rows
def processChatSession(zwachatsession_row):
    session = {}
    session["ID"] = zwachatsession_row["Z_PK"]
    session["messages"] = []
    if zwachatsession_row["ZGROUPINFO"] is None:
        session["type"] = "direct"
        session["contact_name"] = zwachatsession_row["ZPARTNERNAME"]
        session["contact_number"] = processNumber(zwachatsession_row["ZCONTACTJID"])
    else:
        session["type"] = "group"
        session["group_ID"] = zwachatsession_row["ZGROUPINFO"]
        session["group_name"] = zwachatsession_row["ZPARTNERNAME"]
    return session


#This function takes a directory containing a texts sqlite3 database and will return a
#list of contacts dictionaries, with each contact having a list of messages
def extractBackup(directory):
    #Get the contacts in this backup
    contacts = sms.extractContacts(directory)

    #Connect to the correct whatsapp database
    if "1b6b187a1b60b9ae8b720c79e2c67f472bab09c0" in os.listdir(directory):
        conn = sqlite3.connect("1b6b187a1b60b9ae8b720c79e2c67f472bab09c0")
    else:
        conn = sqlite3.connect("7c7fba66680ef796b916b067077cc246adacf01d")
    c = conn.cursor()

    #Get sqlite_master table
    c.execute("SELECT * FROM sqlite_master;")
    sqlite_master =  c.fetchall()

    #Get the zwamessage table
    zwamessage_keys = sms.getKeys(sqlite_master, "ZWAMESSAGE")
    c.execute("SELECT * FROM ZWAMESSAGE;")
    zwamessage = c.fetchall()
    zwamessage = [dict(zip(zwamessage_keys, m)) for m in zwamessage]
    print("There are " + str(len(zwamessage)) + " messages in this backup")
    
    #Get the zwachatsession table
    zwachatsession_keys = sms.getKeys(sqlite_master, "ZWACHATSESSION")
    c.execute("SELECT * FROM ZWACHATSESSION;")
    zwachatsession = c.fetchall()
    zwachatsession = [dict(zip(zwachatsession_keys, m)) for m in zwachatsession]
    print("There are " + str(len(zwachatsession)) + " chat sessions in this backup")
    
    #Get the zwagroupinfo table
    zwagroupinfo_keys = sms.getKeys(sqlite_master, "ZWAGROUPINFO")
    c.execute("SELECT * FROM ZWAGROUPINFO;")
    zwagroupinfo = c.fetchall()
    zwagroupinfo = [dict(zip(zwagroupinfo_keys, m)) for m in zwagroupinfo]
    print(str(len(zwagroupinfo)) + " of these are group chats")
                                                           
    #Get the zwagroupmember table                                    
    zwagroupmember_keys = sms.getKeys(sqlite_master, "ZWAGROUPMEMBER")
    c.execute("SELECT * FROM ZWAGROUPMEMBER;")
    zwagroupmember = c.fetchall()
    zwagroupmember = [dict(zip(zwagroupmember_keys, m)) for m in zwagroupmember]
    
    #Turn the raw zwamessage list into a cleaned up messages list
    messages = [processMessage(m) for m in zwamessage]
    messages = [m for m in messages if m["message_type"] != 6]
    print("There are " + str(len(messages)) + " messages after removing type 6 messages")

    #Also clean up chat sessions (don't really need zwagroupinfo so don't bother with that)
    chat_sessions = [processChatSession(c) for c in zwachatsession]

    #Assign the direct messages and report what's left
    for message in messages:
        assigned = False
        for session in chat_sessions:
            if session["type"] == "direct" and message["chat_session"] == session["ID"]:
                message.update({"weight":1})
                session["messages"].append(message)
                assigned = True
        if not assigned:
            message.update({"weight":"group"})
    print(str(len([m for m in messages if m["weight"] == 1])) + " messages were assigned to direct chats and there are " + str(len([m for m in messages if m["weight"] == "group"])) + " messages unassigned")

    #Assign the direct messages to contacts
    for session in [c for c in chat_sessions if c["type"] == "direct"]:
        assigned = False
        for contact in contacts:
            if session["contact_number"] in contact["numbers"]:
                print("Assigning to " + session["contact_name"])
                contact["messages"] += session["messages"]
                assigned = True
        if not assigned: print("Could not assign " + session["contact_name"])

    #Now for the group messages - first assign each one to its group chat
    group_assigned = 0
    for message in messages:
        for session in chat_sessions:
            if session["type"] == "group" and message["chat_session"] == session["ID"]:
                session["messages"].append(message)
                group_assigned += 1
    print(str(group_assigned) + " messages have been assigned to group chats")

    #These messages will have INCORRECT sender information - correct this using info from zwagroupinfo:
    for session in chat_sessions:
        if session["type"] == "group":
            for message in session["messages"]:
                if not message["from_me"]:
                    for member in zwagroupmember:
                        if member["Z_PK"] == message["group_member"]:
                            message["sender"] = processNumber(member["ZMEMBERJID"])

    #Give each group session a list of numbers involved
    for group in chat_sessions:
        if group["type"] == "group":
            group["members"] = []
            for message in group["messages"]:
                group["members"].append(message["sender"])
            group["members"] = list(set(group["members"]))

    #Now go through each contact and, if they appear in any of the groups, assign all messages with correct weight
    for person in contacts:
        for session in chat_sessions:
            if session["type"] == "group" and bool(set(session["members"]).intersection(set(person["numbers"]))):
                for message in session["messages"]:
                    message.update({"group":True})
                    person["messages"].append(dict(message))
                    if message["sender"] == my_number or message["sender"] in person["numbers"]:
                        person["messages"][-1]["weight"] = 1/(len(session["members"])-1)
                    else:
                        person["messages"][-1]["weight"] = 0
                




    contacts = [c for c in contacts if len(c["messages"]) > 0 and c["name"] != "Sam Ireland"]

    #Finish sorting out the group sender field
    for person in contacts:
        for message in person["messages"]:
            if message["from_me"]:
                message["sender"] = "Sam Ireland"
                message["receiver"] = person["name"]
            else:
                if message["group"]:
                    for entry in zwagroupmember:
                        if message["sender"] == processNumber(entry["ZMEMBERJID"]):
                            message["sender"] = entry["ZCONTACTNAME"]
                            break
                else:
                    message["sender"] = person["name"]
                message["receiver"] = "Sam Ireland"
        
    return contacts


#Same as SMS really
def get_all_whatsapp(directory):
    backup_names = [d for d in os.listdir(directory) if "." not in d and d != "html"]
    print("Found " + str(len(backup_names)) + " backups: " + ", ".join(backup_names))
    recipient = []
    
    #Get the backups
    backups = []
    for backup in backup_names:
        print("")
        backups.append(extractBackup(directory + "\\" + backup))

    if len(backups) > 1:
        #Merge them together
        recipient = backups[1]
        for x in range(len(backups)):
            if x != 1:
                recipient = sms.merge_two_backups(backups[x] ,recipient)
    #recipient should now be the finalised contacts object - clean it up and we can be on our way!
    people = [r for r in recipient if len(r["messages"]) > 0]
    for person in people:
        sms.sortMessages(person)
        for message in person["messages"]:
            person["message_count"] += message["weight"]
            if message["text"] is None:
                person["message_length_count"] += 0
            else:
                person["message_length_count"] += (len(message["text"]) * message["weight"])
            
    people = sorted(people, key=lambda k: k["message_length_count"], reverse=True)

    return people

if __name__ == "__main__":
    import pickle
    location = input("Where is the backup loacated? ")
    file_name = input("What shall the dump be called? ")
    if file_name[-2:] == ".p": file_name = file_name[:-2]
    print("")
    
    data = get_all_whatsapp(location)

    f = open(location + "\\" + file_name + ".p", "wb")
    pickle.dump(data, f)
