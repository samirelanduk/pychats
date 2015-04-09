def printHeader(s):
    if len(s) % 2 != 0:
        s += " "
    print("*" * (6 + len(s)))
    print("*" + (" " * (4 + len(s))) + "*")
    print("*  " + s + "  *")
    print("*" + (" " * (4 + len(s))) + "*")
    print("*" * (6 + len(s)))
    print("\n\n")

printHeader("SMS")
import sms
printHeader("WhatsApp")
import whatsapp
printHeader("Facebook")
import facebook

printHeader("MERGING")
print("Attempting merger of sms and whatsapp...")

folks = []
toRemoveS = []
toRemoveW = []
for w in whatsapp.people:
    for s in sms.sms_backup:
        if w["name"] == s["name"]:
            print("\tMerging " + w["name"])
            f = {}
            f["name"] = w["name"]
            f["messages"] = []
            smsM = s["messages"]
            whaM = w["combinedMessages"]
            for sm in smsM:
                sm.update({"type":"sms"})
            for wm in whaM:
                wm.update({"type":"whatsapp"})
            f["messages"] += smsM
            f["messages"] += whaM
            folks.append(f)
            toRemoveS.append(s)
            toRemoveW.append(w)

while len(toRemoveS) > 0:
    sms.sms_backup.remove(toRemoveS.pop())

while len(toRemoveW) > 0:
    whatsapp.people.remove(toRemoveW.pop())

for c in sms.sms_backup:
    f = {}
    f["name"] = c["name"]
    f["messages"] = c["messages"]
    for m in f["messages"]:
        m.update({"type":"sms"})
    folks.append(f)

for c in whatsapp.people:
    f = {}
    f["name"] = c["name"]
    f["messages"] = c["combinedMessages"]
    for m in f["messages"]:
        m.update({"type":"whatsapp"})
    folks.append(f)

print("Attempting merger with facebook.")
toRemoveF = []
for f in folks:
    for fb in facebook.contacts:
        if f["name"] == fb["name"]:
            print("\tMerging " + f["name"])
            for m in fb["combinedMessages"]:
                m.update({"type":"facebook"})
                f["messages"].append(m)
            toRemoveF.append(fb)
        
while len(toRemoveF) > 0:
    facebook.contacts.remove(toRemoveF.pop())

stillMerging = True
while stillMerging:
    longestName = max([len(c["name"]) for c in facebook.contacts])     
    for x in range(max(len(facebook.contacts),len(facebook.contacts))):
        line = ""
        if x < len(facebook.contacts): line = str(x) + ": " + facebook.contacts[x]["name"] + (" "*(longestName-len(facebook.contacts[x]["name"])))
        else: line = "\t\t"
        if x < len(folks): line += "\t\t" + str(x) + ": " + folks[x]["name"]
        print(line)

    user_input = input("\nCan we merge any of the above contacts? Same drill (left,right) if so, any other format if not. ")
    if user_input.count(",") == 1 and user_input.split(",")[0].isnumeric() and "." not in user_input.split(",")[0] and int(user_input.split(",")[0]) <= len(facebook.contacts) and user_input.split(",")[1].isnumeric() and "." not in user_input.split(",")[1] and int(user_input.split(",")[1]) <= len(folks):
        left = int(user_input.split(",")[0])
        right = int(user_input.split(",")[1])
        folks[right]["messages"] += facebook.contacts[left]["combinedMessages"]
        facebook.contacts.remove(facebook.contacts[left])
    else:
        stillMerging = False

for person in facebook.contacts:
    f = {}
    f["name"] =
    person["name"]
    f["messages"] = []
    for m in person["combinedMessages"]:
        m.update({"type":"facebook"})
        f["messages"].append(m)
    folks.append(f)
        
        

for person in folks:
    person["messages"] = sorted(person["messages"], key=lambda k: k['time'])
    person["num"] = 0
    for m in person["messages"]:
        person["num"] += m["weight"]

folks = sorted(folks, key=lambda k: k["num"])
folks.reverse()

