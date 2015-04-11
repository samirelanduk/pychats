import sms
import whatsapp
import pickle

directory = input("Directory: ")

sms_contacts = sms.get_all_SMS(directory)
whatsapp_contacts = whatsapp.get_all_whatsapp(directory)

folks = sms.merge_two_backups(sms_contacts, whatsapp_contacts)

for person in folks:
    sms.sortMessages(person)
    for message in person["messages"]:
            person["message_count"] += message["weight"]
            if message["text"] is None:
                person["message_length_count"] += 0
            else:
                person["message_length_count"] += (len(message["text"]) * message["weight"])
                
folks = sorted(folks, key=lambda k: k["message_length_count"], reverse=True)

f = open(directory + "\\" + input("Dump name: "), "wb")
pickle.dump(folks, f)
