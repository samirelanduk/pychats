"""This module provides the functions for parsing Faceboom backup
messages.htm files."""

from bs4 import BeautifulSoup

def html_to_threads(html):
    """Takes the html string of a file and gets the thread divs from it as
    ``BeautifulSoup`` Tag objects.

    :param str html: The HTML string."""

    if not isinstance(html, str):
        raise TypeError("HTML must be provided as a string")
    soup = BeautifulSoup(html, "html.parser")
    threads = soup.find_all("div", {"class" : "thread"})
    return threads
