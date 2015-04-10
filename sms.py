import sqlite3
import datetime
import os

#This function takes an sqlite_master tabke and gets a specified table's keys from it as a list
def getKeys(master, name):
    table = [row for row in master if row[0] == "table" and row[1] == name][0]
    keys = table[4]
    keys = keys.split(name + " (")[1][:-1].lstrip()
    return [key.split(" ")[0] for key in keys.split(", ")]


#This function takes an abperson row and returns a cleaned up contact dictionary
def getContact(contact_row):
    contact = {}
    contact["name"] = contact_row["First"]
    if contact_row["Last"] != None:
        contact["name"] += " " + contact_row["Last"]
    contact["ID"] = contact_row["ROWID"]
    contact["numbers"] = []
    contact["messages"] = []
    contact["message_count"] = 0
    contact["message_length_count"] = 0
    return contact


#This function takes a phone number and forces it into a standard format: +LLNNNNNNNNNN
def sanitise_number(number_string):
    sanitised = number_string.replace(" ","")
    if sanitised[0] == "0":
        sanitised = "+44" + sanitised[1:]
    return sanitised


#This function will take a directory containing a contacts sqlite3 database, and return the pertinent
#information as a list of dictionaries
def extractContacts(directory):
    backup_name = directory.split("\\")[-1]
    
    #Connect to database
    os.chdir(directory)
    conn = sqlite3.connect("31bb7ba8914766d4ba40d6dfb6113c8b614be442")
    c = conn.cursor()

    #Get sqlite_master table
    c.execute("SELECT * FROM sqlite_master;")
    sqlite_master =  c.fetchall()

    #Get the ABPerson table
    abperson_keys = getKeys(sqlite_master, "ABPerson")
    c.execute("SELECT * FROM ABPerson;")
    abperson = c.fetchall()
    abperson = [dict(zip(abperson_keys, abp)) for abp in abperson]
    print("There are " + str(len(abperson)) + " contacts in backup " + backup_name)

    #Get the ABMultiValue table (and remove values that aren't phone numbers)
    abmultivalue_keys = getKeys(sqlite_master, "ABMultiValue")
    c.execute("SELECT * FROM ABMultiValue;")
    abmultivalue = c.fetchall()
    abmultivalue = [dict(zip(abmultivalue_keys, abmv)) for abmv in abmultivalue]
    abmultivalue = [abmv for abmv in abmultivalue if abmv["value"] != None and abmv["value"].replace(" ","").replace("+","").isnumeric()]
    print("There are " + str(len(abmultivalue)) + " phone numbers in backup " + backup_name)

    #Get a list of contacts, each with ID and numbers
    contacts = [getContact(abp) for abp in abperson]
    unknown_numbers = []
    found = 0
    for abmv in abmultivalue:
        assigned = False
        for contact in contacts:
            if abmv["record_id"] == contact["ID"]:
                contact["numbers"].append(sanitise_number(abmv["value"]))
                found += 1
                assigned = True
        if not assigned:
            unknown_numbers.append(abmv["value"])
    print(str(found) + " numbers have been assigned to contacts")
    print(str(len(unknown_numbers)) + " numbers could not be assigned")
    print("")
    return contacts


#This funtction takes a row from message table and returns a cleaned up dictionary
def processMessage(message_row):
    message = {}
    message["text"] = message_row["text"]
    message["handle"] = message_row["handle_id"]
    message["time"] = datetime.datetime.utcfromtimestamp(message_row["date"]+978307200)
    message["from_me"] = bool(message_row["is_from_me"])
    message["type"] = "SMS"
    return message


#This function takes a contact with no name, and a list of named contacts, and tries to assign the nameless one
#by showing its messages and asking for a name
def try_assign(unknown, knowns):
    messages_to_use = unknown["messages"]
    if len(messages_to_use) > 20:
        messages_to_use = messages_to_use[-18:]
    print("\n------")
    for mtu in messages_to_use:
        m = ""
        if mtu["from_me"]:
            m += "Me: "
        else:
            m += "Them: "
        m += mtu["text"]
        print(m)
    print("------")
    name = input("Where should the above go? Name, or '.' to delete. ")
    if name != ".":
        if name in [k["name"] for k in knowns]:
            for k in knowns:
                if k["name"] == name:
                    k["messages"].append(unknown["messages"])
        else:
            knowns.append({"name":name, "numbers": [unknown["number"]], "messages":unknown["messages"]})
    print("")


#This function checks a string is in the format 'x,y' where x and y are smaller than m1 and m2 respectively
def checkEntry(s, m1, m2):
    if s.count(",") == 1 and s.split(",")[0].isnumeric() and int(s.split(",")[0]) <= m1 and s.split(",")[1].isnumeric() and int(s.split(",")[1]) <= m2:
        return True
    else:
        return False
        

#This function takes a list of dictionaries with a name key and message list, and asks the user if they want to merge any
def deduplicate(l):
    allFine = False
    while not allFine:
        print("")
        x = 0
        for item in l:
            print(str(x) + ": " + item["name"])
            x += 1
        response = input("Are any of the above duplicates? Enter their two IDs if so (x,y), anything else if it's all fine. ")
        if checkEntry(response, x, x):
            first,second = [int(n) for n in response.split(",")]
            l[first]["messages"] += l[second]["messages"]
            l[first]["numbers"] += l[second]["numbers"]
            l.remove(l[second])
        else:
            allFine = True

#This function takes a directory containing a texts sqlite3 database and will return a
#list of contacts dictionaries, with each contact having a list of messages
def extractBackup(directory):
    backup_name = directory.split("\\")[-1]

    #Get a list of the contacts in this backup
    contacts = extractContacts(directory)

    #Connect to database
    os.chdir(directory)
    conn = sqlite3.connect("3d0d7e5fb2ce288813306e4d4636395e047a3d28")
    c = conn.cursor()

    #Get sqlite_master table
    c.execute("SELECT * FROM sqlite_master;")
    sqlite_master =  c.fetchall()

    #Get the message table
    message_keys = getKeys(sqlite_master, "message")
    c.execute("SELECT * FROM message;")
    message = c.fetchall()
    message = [dict(zip(message_keys, m)) for m in message]
    print("There are " + str(len(message)) + " messages in backup " + backup_name)

    #Get the handle table
    handle_keys = getKeys(sqlite_master, "handle")
    c.execute("SELECT * FROM handle;")
    handle = c.fetchall()
    handle = [dict(zip(handle_keys, h)) for h in handle]
    print("There are " + str(len(handle)) + " handles in backup " + backup_name)

    #Turn the raw message list into a cleaned up messages list
    messages = [processMessage(m) for m in message]

    #Give each message a phone number
    lost_messages = []
    for m in messages:
        if m["handle"] == 0:
            lost_messages.append(m)
        else:
            for h in handle:
                if m["handle"] == h["ROWID"]:
                    m["number"] = h["id"]
    for lm in lost_messages:
        messages.remove(lm)

    print(str(len(lost_messages)) + " messages had no phone number attached and have been removed")

    #Add each message to its proper contact
    unassigned_messages = []
    assigned_messages = 0
    for m in messages:
        assigned = False
        for c in contacts:
            if m["number"] in c["numbers"]:
                c["messages"].append(m)
                assigned = True
                assigned_messages += 1
        if not assigned:
            unassigned_messages.append(m)
    print(str(assigned_messages) + " have been assigned to a contact")
    print(str(len(unassigned_messages)) + " could not be assigned")

    #Get rid of unassigned messages that are probably spam
    unassigned_messages = [um for um in unassigned_messages if not um["number"].isalpha() and len(um["number"]) > 6]
    print(str(len(unassigned_messages)) + " unassigned message remaining after screen")

    #Get a list of unknown numbers from the unassigned messages
    unknown_numbers = list(set([um["number"] for um in unassigned_messages]))

    #Make a sort of contacts list for these unknown people
    unknown_contacts = [{"number":un, "messages":[]} for un in unknown_numbers]
    for um in unassigned_messages:
        for uc in unknown_contacts:
            if um["number"] == uc["number"]:
                uc["messages"].append(um)
    unknown_contacts = [uc for uc in unknown_contacts if len(uc["messages"]) > 1]
    print("These unassigned messages belong to " + str(len(unknown_contacts)) + " numbers")
    
    #For each unknown person, either them to the contacts undera given name, or get rid of them
    for uc in unknown_contacts:
        try_assign(uc, contacts)

    #After all that, there might be some contacts taking up two entries. Resolve this.
    deduplicate(contacts)

    #All done! Message sorting and field policing can be done later
    print("")
    return contacts


#This function takes two backups and merges them. Backup must be a list of dictionaries with each dict having messages
def merge_two_backups(b1, b2):
    #Attempt automatic merger
    toRemove = []
    for p1 in b1:
        for p2 in b2:
            if p1["name"] == p2["name"]:
                print("merging " + p1["name"])
                p2["messages"] += p1["messages"]
                p2["numbers"] += p1["numbers"]
                toRemove.append(p1)
                break
    while len(toRemove) > 0:
        b1.remove(toRemove.pop())
        
    #Ask for manual merge
    still_merging = True
    while still_merging:
        longestName = max([len(c["name"]) for c in b1])
        print(longestName)
        for x in range(max(len(b1),len(b2))):
            if x < len(b1):
                print(str(x) + ":" + b1[x]["name"] + (" " * (longestName - len(b1[x]["name"]))), end=" ")
            else:
                print((" " * longestName), end=" ")
            if x < len(b2):
                print("\t\t" + str(x) + ": " + b2[x]["name"])
        response = input("\nDo any of the above need merging? Format (left,right): ")
        if checkEntry(response, len(b1)-1, len(b2)-1):
            left, right = [int(n) for n in response.split(",")]
            b2[right]["messages"] += b1[left]["messages"]
            b2[right]["numbers"] += b1[left]["numbers"]
            b1.remove(b1[left])
        else:
            still_merging = False
    return b2
    

#This function takes a contact and sorts their messages by time
def sortMessages(contact):
    contact["messages"] = sorted(contact["messages"], key=lambda k: k["time"])

#This function processes a set of backups and merges them
def get_all_SMS(directory):
    backup_names = [d for d in os.listdir(directory) if "." not in d]
    print("Found " + str(len(backup_names)) + " backups: " + ", ".join(backup_names))

    #Get the backups
    backups = []
    for backup in backup_names:
        print("")
        backups.append(extractBackup(directory + "\\" + backup))

    if len(backups) > 1:
        #Merge them together
        recipient = backups[1]
        for x in range(len(backups)-1):
            recipient = merge_two_backups(backups[x] ,recipient)

    #recipient should now be the finalised contacts object - clean it up and we can be on our way!
    people = [r for r in recipient if len(r["messages"]) > 0]
    for person in people:
        sortMessages(person)
        for message in person["messages"]:
            person["message_count"] += 1
            if message["text"] is None:
                person["message_length_count"] += 0
            else:
                person["message_length_count"] += len(message["text"])
            if message["from_me"]:
                message["sender"] = "Sam Ireland"
                message["receiver"] = person["name"]
            else:
                message["receiver"] = "Sam Ireland"
                message["sender"] = person["name"]
    people = sorted(people, key=lambda k: k["message_length_count"], reverse=True)

    return people


def printDict(d):
    for key in d.keys():
        print(str(key) + ": " + str(d[key]))
    print("")

if __name__ == "__main__":
    import pickle
    location = input("Where is the backup loacated? ")
    file_name = input("What shall the dump be called? ")
    print("")
    
    data = get_all_SMS(location)

    f = open(location + "\\" + file_name + ".p", "wb")
    pickle.dump(data, f)
