def facebook_backup(file, my_name=""):
    from . import facebook
    from bs4 import BeautifulSoup

    #Need to know user's Facebook name
    if my_name == "":
        my_name = input("What is your Facebook name? ")

    #Open the file to get the html
    html = file.read()
    print("Getting soup (can take a few seconds)...")
    soup = BeautifulSoup(html)

    #Get conversations
    conversations = facebook.get_conversations(soup, my_name)

    return conversations

class Backup:
    pass

class Contact:
    pass

class Message:
    pass
