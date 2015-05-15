import sms
import whatsapp
import pickle
import facebook

directory = input("Directory: ")

def madeEarlier(func, d):
    if input("Is there a pre-made file? (Y/N) ").lower() == "y":
        f = open(input("File: "), "rb")
        obj = pickle.load(f)
        return obj
    else:
        obj = func(d)
        return obj

print("SMS:")    
sms_contacts = madeEarlier(sms.get_all_SMS, directory)
print("Whatsapp:")
whatsapp_contacts = madeEarlier(whatsapp.get_all_whatsapp, directory)

folks = sms.merge_two_backups(whatsapp_contacts, sms_contacts)

print("Facebook:")
facebook_contacts = madeEarlier(facebook.get_all_facebook, directory)

folks = sms.merge_two_backups(facebook_contacts, folks)

for person in folks:
    sms.sortMessages(person)
    person["message_count"] = 0
    person["message_length_count"] = 0
    for message in person["messages"]:
            person["message_count"] += message["weight"]
            if message["text"] is None:
                person["message_length_count"] += 0
            else:
                person["message_length_count"] += (len(message["text"]) * message["weight"])
                
folks = sorted(folks, key=lambda k: k["message_length_count"], reverse=True)

#Name changes?
stillChanging = True
while stillChanging:
    print("")
    for x in range(len(folks)):
        print(str(x) + ": " + folks[x]["name"])
    print("")
    response = input("Change a name? ID,name or '.' to move on (NO ERROR CHECKING HERE) ")
    if response == ".":
        stillChanging = False
    else:
        ID,new_name = response.split(",")[0],response.split(",")[1]
        folks[int(ID)]["name"] = new_name

#Delete the wastes of space
print("")
for x in range(len(folks)):
    print(str(x) + ": " + folks[x]["name"])
print("")
deletees = input("IDs of people to be deleted. No error checking again so don't try anything stupid: ")
IDs = [int(x) for x in deletees.split(",")]
to_delete = [folks[x] for x in IDs]
while len(to_delete) > 0:
    folks.remove(to_delete.pop())

f = open(directory + "\\" + input("Dump name: "), "wb")
pickle.dump(folks, f)
