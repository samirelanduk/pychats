import sqlite3
import datetime
import os
import time

def formatTelnum(numString):
    numString = numString.replace(" ","")
    if numString[0] == "0":
        numString = "+44" + numString[1:]
    return numString

def getTable(conn, name):
    c = conn.cursor()
    c.execute("SELECT * FROM sqlite_master;")
    master = c.fetchall()
    info = 0
    for item in master:
        if item[1] == name:
            info = item
    length = len("CREATE TABLE " + name) + 3
    keys = info[4][length:-2].split(", ")
    c.execute("SELECT * FROM " + name + ";")
    table = c.fetchall()
    table = [dict(zip(keys,t)) for t in table]
    return table

def getName(ID, contacts):
    num = "+" + ID.split("@")[0].split("-")[0]
    name = num
    for c in contacts:
        if num in c["numbers"]: name = c["name"]
    return name
        
def printTable(table):
    for item in table:
        for k in item.keys():
            print(k + ": " + str(item[k]))
        print("")


#dirname = input("Directory: ")
dirname = "C:\\Users\\Sam\\OneDrive\\7) Computing\\Programming\\Python projects\\5 - Message history\\backups"
os.chdir(dirname)

backups = []
for directory in [f for f in os.listdir(".") if "." not in f]:
    os.chdir(directory)
    print("Starting " + directory + " whatsapp")
    time.sleep(2)

    #Get a list of contacts
    conn = sqlite3.connect("31bb7ba8914766d4ba40d6dfb6113c8b614be442")
    c = conn.cursor()
    c.execute("SELECT * FROM sqlite_master;")
    sqlite_master = c.fetchall()
    c.execute("SELECT * FROM abperson;")
    abperson = c.fetchall()
    c.execute("SELECT * FROM ABMultivalue;")
    abmultivalue = c.fetchall()
    conn.close()

    contacts = [{"name": "Sam Ireland", "ID":0, "numbers":["+447825232871"]}]
    for person in abperson:
        contact = person[1]
        if person[2] != None: contact = contact + " " + person[2]
        contacts.append({"name": contact, "ID": person[0], "numbers":[]})

    for mv in abmultivalue:
        for contact in contacts:
            if mv[1] == contact["ID"]:
                if mv[5] != None and "@" not in mv[5]: contact["numbers"].append(formatTelnum(mv[5]))

    #Get whatsapp messages
    if "1b6b187a1b60b9ae8b720c79e2c67f472bab09c0" in os.listdir("."):
        conn = sqlite3.connect("1b6b187a1b60b9ae8b720c79e2c67f472bab09c0")
    else:
        conn = sqlite3.connect("7c7fba66680ef796b916b067077cc246adacf01d")

    zwamessage = getTable(conn, "ZWAMESSAGE")
    zwachatsession = getTable(conn, "ZWACHATSESSION")
    zwagroupinfo = getTable(conn, "ZWAGROUPINFO")
    conn.close()

    for m in zwamessage:
        if m["ZTOJID VARCHAR"] != None: m["ZTOJID VARCHAR"] = getName(m["ZTOJID VARCHAR"], contacts)
        if m["ZFROMJID VARCHAR"] != None: m["ZFROMJID VARCHAR"] = getName(m["ZFROMJID VARCHAR"], contacts)

    for c in zwachatsession:
        c["ZCONTACTJID VARCHAR"] = getName(c["ZCONTACTJID VARCHAR"], contacts)

    for g in zwagroupinfo:
        g["ZOWNERJID VARCHAR"] = getName(g["ZOWNERJID VARCHAR"], contacts)

    chats = len(zwachatsession)
    groups = len(zwagroupinfo)
    groups2 = len([c for c in zwachatsession if c["ZGROUPINFO INTEGER"] != None])

    print("\tThere are " + str(chats) + " chats.")
    print("\tThere are " + str(groups) + " group chats.")
    print("\tThere are " + str(groups2) + " group chats.")
    print("\tGroup chat names: ")
    for chat in [c for c in zwachatsession if c["ZGROUPINFO INTEGER"] != None]:
        try:
            print("\t\t" + str(chat["ZPARTNERNAME VARCHAR"]))
        except:
            print("\t\t<unprintable>")

    chatsessions = []
    for c in zwachatsession:
        session = {}
        if c["ZGROUPINFO INTEGER"] == None:
            session["type"] = "direct"
            session["contact"] = c["ZCONTACTJID VARCHAR"]
        else:
            session["type"] = "group"
            session["group_name"] = c["ZPARTNERNAME VARCHAR"]
        session["chat_ID"] = c["Z_PK INTEGER PRIMARY KEY"]
        session["messages"] = []
        chatsessions.append(session)
    groups = [c for c in chatsessions if c["type"] == "group"]
    directs = [c for c in chatsessions if c["type"] == "direct"]

    for m in zwamessage:
        message = {}
        if m["ZTEXT VARCHAR"] == None:
             message["text"] = "<<<NONE_TEXT>>>"
        else:
            message["text"] = m["ZTEXT VARCHAR"]
        message["time"] = datetime.datetime.utcfromtimestamp(m["ZMESSAGEDATE TIMESTAMP"]+978264705)
        if m["ZTOJID VARCHAR"] != None:
            message["recipient"] = m["ZTOJID VARCHAR"]
        if m["ZFROMJID VARCHAR"] != None:
            message["sender"] = m["ZFROMJID VARCHAR"]
        else:
            message["sender"] = "Sam Ireland"
        for g in groups:
            if g["chat_ID"] == m["ZCHATSESSION INTEGER"]:
                g["messages"].append(message)
        for d in directs:
            if d["chat_ID"] == m["ZCHATSESSION INTEGER"]:
                d["messages"].append(message)

    for d in directs:
        name = d["messages"][0]["sender"]
        if name == "Sam Ireland":
            name = d["messages"][0]["recipient"]
        d["contact"] = name

    for g in groups:
        g["members"] = []
        for m in g["messages"]:
            g["members"].append(m["sender"])
            if "recipient" in m:
                del m["recipient"]
        g["members"] = list(set(g["members"]))
        if "Sam Ireland" in g["members"]: g["members"].remove("Sam Ireland")

    whatsapp_contacts = [{"name":d["contact"], "combinedMessages":[], "num":0} for d in directs if d["contact"] != "+Server"]
    for wc in whatsapp_contacts:
        for d in directs:
            if wc["name"] == d["contact"]:
                for message in  d["messages"]:
                    m = message
                    m.update({"weight":1})
                    wc["combinedMessages"].append(m)
        for g in groups:
            if wc["name"] in g["members"]:
                for message in g["messages"]:
                    m = message
                    weight = 0
                    if m["sender"] == "Sam Ireland" or m["sender"] == wc["name"]:
                        weight = 1/len(g["members"])
                    m.update({"weight":weight})
                    wc["combinedMessages"].append(m)
    backups.append(whatsapp_contacts)
    os.chdir("..")


#Now try and merge the backups together
toRemove = []
for b in range(len(backups)-1):
    for c1 in backups[b]:
        for c2 in backups[b+1]:
            if c1["name"] == c2["name"]:
                print("\tMerging " + c1["name"])
                c2["combinedMessages"] += c1["combinedMessages"]
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
            backups[b+1][right]["combinedMessages"] += backups[b][left]["combinedMessages"]
            backups[b].remove(backups[b][left])
        else:
            stillMerging = False

people = []
for b in backups:
    people += b

for person in people:
    person["combinedMessages"] = sorted(person["combinedMessages"], key=lambda k:k["time"])
    for cm in person["combinedMessages"]:
        person["num"] += cm["weight"]

people = sorted(people, key=lambda k: k["num"])
people.reverse()
