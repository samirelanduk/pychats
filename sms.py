import sqlite3
import datetime
import os

#dirname = input("Directory: ")
dirname = "C:\\Users\\Sam\\OneDrive\\7) Computing\\Programming\\Python projects\\5 - Message history\\backups"
os.chdir(dirname)

def formatTelnum(numString):
    if numString != None:
        numString = numString.replace(" ","")
        if numString[0] == "0":
            numString = "+44" + numString[1:]
    return numString

def sender(x):
    if x == 0: return "Them"
    elif x == 1: return "Sam"
    else: return "Unknown"

def deleteEmptyContacts(contacts):
    empties = []
    for c in contacts:
        if len(c["messages"]) == 0 or (type("") == type(c["number"]) and len(c["number"]) < 7):
            empties.append(c)
            if "name" in c.keys():
                print("Deleting " + c["name"])
            else:
                print("Deleting _nameless")
    while len(empties) != 0:
        contacts.remove(empties.pop())
    return contacts

def sanitise(messages):
    for message in messages:
        if message["text"] == None:
            message["text"] = ""
        else:
            text = list(message["text"])
            x = 0
            for char in text:
                if len(bytes(char, "UTF-8")) >= 4:
                    text[x] = "�"
                x += 1
            message["text"] = "".join(text)
        message["weight"] = 1
    return messages
            

backups = []
for directory in [f for f in os.listdir(".") if "." not in f]:
    os.chdir(directory)

    #Get a list of contacts
    conn = sqlite3.connect("31bb7ba8914766d4ba40d6dfb6113c8b614be442")
    c = conn.cursor()
    c.execute("SELECT * FROM abperson;")
    abperson = c.fetchall()
    c.execute("SELECT * FROM ABMultivalue;")
    abmultivalue = c.fetchall()
    conn.close()
    contacts = []
    for person in abperson:
        contact = person[1]
        if person[2] != None: contact = contact + " " + person[2]
        contacts.append({"name":contact, "number":person[0], "handles":[], "messages":[]})

    for c in contacts:
        mvs = [formatTelnum(mv[5]) for mv in abmultivalue if mv[1] == c["number"]]
        while None in mvs:
            mvs.remove(None)
        c["number"] = mvs

    #Now get all the texts
    conn = sqlite3.connect("3d0d7e5fb2ce288813306e4d4636395e047a3d28")
    c = conn.cursor()
    c.execute("SELECT * FROM message;")
    message = c.fetchall()
    c.execute("SELECT * FROM handle;")
    handle = c.fetchall()
    conn.close()

    #Add handle info to the contacts
    for handl in handle:
        for person in contacts:
                if formatTelnum(handl[1]) in person["number"]:
                    person["handles"].append(handl[0])

    messages = [{"handle":m[5], "sender":sender(m[21]), "time":datetime.datetime.utcfromtimestamp(m[15]+978307200), "text":m[2], "transfered":False} for m in message]
    for m in messages:
        for c in contacts:
            if m["handle"] in c["handles"]:
                m["transfered"] = True
                c["messages"].append(m)
    not_moved = [m for m in messages if not m["transfered"]]
    unknown_numbers = []
    for m in not_moved:
        for handl in handle:
            if m["handle"] == handl[0]: unknown_numbers.append(handl[1])
    unknown_numbers = list(set(unknown_numbers))
    unknown_numbers = [{"number":u, "messages":[]} for u in unknown_numbers]
    for m in not_moved:
        for handl in handle:
            if m["handle"] == handl[0]:
                for u in unknown_numbers:
                    if u["number"] == handl[1]:
                        u["messages"].append(m)
    unknown_numbers = deleteEmptyContacts(unknown_numbers)
    contacts = deleteEmptyContacts(contacts)

    
    #Try and allocate the unknown numbers
    for u in unknown_numbers:
        if not u["number"].isalpha():
            if len(u["messages"]) > 20:
                print(u["messages"][-19:], end="\n\n")
            else:
               print(u, end="\n\n")
            name = input("Where is this mess going? Press _ to delete them. ")
            if name != "_":
                contacts.append({"name": name, "info": [u["number"]], "handles":[0], "messages":u["messages"]})

    stillMerging = True
    while stillMerging:
        x = 0
        for c in contacts:
            print(str(x) + ": " + c["name"])
            x += 1
        user_input = input("\nDo you want to merge any of the above contacts? If YES, enter their two IDs , seperated by a comma (recip, donor). If NO, enter something else. ")
        if user_input.count(",") == 1 and user_input.split(",")[0].isnumeric() and "." not in user_input.split(",")[0] and int(user_input.split(",")[0]) <= x and user_input.split(",")[1].isnumeric() and "." not in user_input.split(",")[1] and int(user_input.split(",")[1]) <= x:
            recipient = int(user_input.split(",")[0])
            donor = int(user_input.split(",")[1])
            for message in contacts[donor]["messages"]:
                contacts[recipient]["messages"].append(message)
            contacts.remove(contacts[donor])
        else:
            stillMerging = False
    print("Appending " + directory.split("//")[-1] + ", " + str(len(contacts)))
    backups.append(contacts)
    os.chdir("..")

print("\nAll backups obtained, attempting automatic merging...")


#Now try and merge the backups together
toRemove = []
for b in range(len(backups)-1):
    for c1 in backups[b]:
        for c2 in backups[b+1]:
            if c1["name"] == c2["name"]:
                print("\tMerging " + c1["name"])
                c2["messages"] += c1["messages"]
                toRemove.append(c1)
    while len(toRemove) != 0:
        backups[b].remove(toRemove.pop())
    print("")
    
    stillMerging = True
    while stillMerging:
        longestName = max([len(c["name"]) for c in backups[b]])     
        for x in range(max(len(backups[b]),len(backups[b+1]))):
            line = ""
            if x < len(backups[b]): line = str(x) + ": " + backups[b][x]["name"] + (" "*(longestName-len(backups[b][x]["name"])))
            else: line = "\t\t"
            if x < len(backups[b+1]): line += "\t\t" + str(x) + ": " + backups[b+1][x]["name"]
            print(line)

        user_input = input("\nCan we merge any of the above contacts? Same drill (left,right) if so, any other format if not. ")
        if user_input.count(",") == 1 and user_input.split(",")[0].isnumeric() and "." not in user_input.split(",")[0] and int(user_input.split(",")[0]) <= len(backups[b]) and user_input.split(",")[1].isnumeric() and "." not in user_input.split(",")[1] and int(user_input.split(",")[1]) <= len(backups[b+1]):
            left = int(user_input.split(",")[0])
            right = int(user_input.split(",")[1])
            backups[b+1][right]["messages"] += backups[b][left]["messages"]
            backups[b].remove(backups[b][left])
        else:
            stillMerging = False

#Combine backups, sanitise messages and sort them all
sms_backup = []
for backup in backups:
    sms_backup += backup

for person in sms_backup:
    person["messages"] = sorted(person["messages"], key=lambda k: k['time'])
    person["messages"] = sanitise(person["messages"])
