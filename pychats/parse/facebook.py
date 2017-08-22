"""This module provides the functions for parsing Facebook backup
messages.htm files."""

from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import datetime
from ..chats.chatlogs import ChatLog

def html_to_threads(html):
    """Takes the html string of a file and gets the thread divs from it as
    ``BeautifulSoup`` Tag objects.

    :param str html: The HTML string.
    :raises TypeError: if non-string HTML is given.
    :returns: ``list`` of ``Tag`` objects"""

    if not isinstance(html, str):
        raise TypeError("HTML must be provided as a string")
    soup = BeautifulSoup(html, "html.parser")
    threads = soup.find_all("div", {"class" : "thread"})
    return threads


def thread_to_json(thread):
    """Takes a Thread div and turns it into the JSON of a
    pychats :py:class:`.Conversation` object.

    :param Tag thread: The ``BeautifulSoup`` Tag of a Facebook thread.
    :rtype: ``list``"""

    if not isinstance(thread, Tag):
        raise TypeError("Need a BeautifulSoup tag, not {}".format(thread))
    messages = thread.find_all("div", {"class" : "message"})
    paragraphs = thread.find_all("p")
    messages = zip(messages, paragraphs)
    json = []
    for message, paragraph in messages:
        name = message.find_all("span", {"class" : "user"})[0].text.strip()
        meta = message.find_all("span", {"class" : "meta"})[0].text.strip()
        date_text = " ".join(meta.split(" ")[:-1])
        date = datetime.strptime(date_text, "%A, %d %B %Y at %H:%M")
        json.append({
         "text": paragraph.text,
         "sender": {"tags": [], "name": name},
         "timestamp": date.strftime("%Y-%m-%d %H:%M:%S")
        })
    return {"messages": json, "members": list(thread.children)[0].strip().split(", ")}


def consolidate_threads(threads):
    """Takes a list of threads JSON objects and combines those which have the
    same members, and which have only two members. It then removes the
    ``members`` key.

    It will also reverse the messages order in each thread.

    :param list threads: The threads to consolidate."""

    for thread in threads:
        thread["members"] = sorted(thread["members"])
    for thread in threads:
        if thread["messages"] and len(thread["members"]) == 2:
            matching_threads = [t for t in threads
             if t["members"] == thread["members"] and thread is not t]
            for matching_thread in matching_threads:
                thread["messages"] += matching_thread["messages"]
                matching_thread["messages"] = []
    threads = [thread for thread in threads if thread["messages"]]
    for thread in threads:
        del thread["members"]
        thread["messages"].reverse()
    return threads


def html_to_chatlog(html):
    """Produces a pychats :py:class:`.ChatLog` from the HTML of a Facebook
    messages.htm filestring

    :param str html: The HTML string.
    :rtype: ``ChatLog``"""

    threads = html_to_threads(html)
    convs = [thread_to_json(thread) for thread in threads]
    convs = consolidate_threads(convs)
    return ChatLog.from_json({"name": "Facebook", "conversations": convs})


def from_facebook(path):
    """Opens a HTML file at the path specified and produces a pychats
    :py:class:`.ChatLog` from it.

    :param str path: The location of the HTML file.
    :rtype: ``ChatLog``"""

    with open(path) as f:
        html = f.read()
    return html_to_chatlog(html)
