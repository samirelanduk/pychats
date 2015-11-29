from bs4 import BeautifulSoup
import datetime
from pychats import ChatLog, Contact, Message

def get_facebook_chatlog(path, my_name, narrate=True):
    """Get a chatlog from a Facebook backup"""

    #Get chatlog soup
    if narrate: print("Processing the backup file (can take a few seconds)...")
    soup = get_chatlog_soup(path)


    #Get all the threads
    if narrate: print("Getting all the threads in this backup...")
    threads = get_threads(soup)
    if narrate: print("There are %i threads here." % len(threads))


    #Who is here?
    if narrate: print("Getting a list of contacts here...")
    names = get_contact_names(threads, my_name)
    if narrate: print("There are %i contacts here." % len(names))


    #Make a contact object out of each of these people
    if narrate: print("Processing these contacts into a finished chatlog...")
    contacts = get_facebook_contacts(names, my_name, threads)


    return ChatLog(contacts, my_name)



def get_chatlog_soup(path):
    """Get soup from the path of a facebook backup"""
    f = open(path, "rb")
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, "html.parser")
    return soup



def get_threads(soup):
    """Takes a facebook backup soup and returns a list of FacebookThread objects"""
    threads = soup.find_all("div", attrs={"class": "thread"})
    threads = [FacebookThread(thread) for thread in threads]

    return threads



def get_contact_names(threads, my_name):
    """Goes through a list of threads and returns the set of contact names therein"""
    names = []
    for thread in threads:
        for name in thread.members:
            if name != my_name and name not in names:
                names.append(name)
    return names



def get_facebook_contacts(names, my_name, threads):
    contacts = []
    for name in names:
        messages = get_facebook_messages(name, my_name, threads)
        contacts.append(Contact(name, messages))

    return contacts



def get_facebook_messages(name, my_name, threads):
    """Get all the messages from a list of threads that a person of a given name has seen"""
    messages = []

    for thread in [t for t in threads if name in t.members]:
        #The person is in this thread
        messages += [FacebookMessage(
         m["text"],
         m["datetime"],
         True if m["sender"] == my_name else False,
         True if m["sender"] == name else False,
         m["sender"] if m["sender"] != name and m["sender"] != my_name else None,
         weight = 0 if m["sender"] != name and m["sender"] != my_name else len(thread.members) - 1
        ) for m in thread.messages]

    return messages



class FacebookThread:
    """A conversation between ourselves and at least one other person"""

    def __init__(self, div):
        #Get a rough idea of the people in this conversation
        self.members = [x for x in div.contents[0].string.split(", ") if "@" not in x]


        #Get the messages as dictionaries (will convert to objects later)
        messages = list(zip(div.contents[1::2], div.contents[2::2]))
        self.messages = [{
         "sender": m[0].find("span", attrs={"class": "user"}).text,
         "datetime": datetime.datetime.strptime(
          m[0].find("span", attrs={"class": "meta"}).text.split("+")[0],
          "%A, %B %d, %Y at %I:%M%p %Z"
         ),
         "text": m[1].text
        } for m in messages]


        #Remove all messages by a '@' person or before January 2011
        self.messages = [x for x in self.messages if
         "@" not in x["sender"] and x["datetime"] > datetime.datetime(2011,1,1)]


        #Put them in the right order
        self.messages.reverse()


        #Add names to members
        for name in set([m["sender"] for m in self.messages]):
            if name not in self.members:
                self.members.append(name)




class FacebookMessage(Message):
    """A Facebook message"""

    name = "Facebook"
    color = "#0000FF"

    def __init__(*args, **kwargs):
        Message.__init__(*args, **kwargs)
