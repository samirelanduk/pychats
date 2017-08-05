"""This module provides the functions for parsing Faceboom backup
messages.htm files."""

from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import datetime

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
    return json
