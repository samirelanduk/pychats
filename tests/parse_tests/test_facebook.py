from unittest import TestCase
from unittest.mock import Mock, patch
import pychats.parse.facebook as fb
from bs4 import BeautifulSoup
from bs4.element import Tag

class HtmlToThreadsTests(TestCase):

    def test_can_convert_html_to_threads_divs(self):
        html = """<html><head><title>Messages</title></head><body>
        <div class="nav"><img src="../photos/profile.jpg"><ul></div>
        <div class="contents"><h1>Name</h1><div>
        <div class="thread">Thread1</div><div class="thread">Thread2</div>
        <div class="thread">Thread3</div></div></body></html>"""
        threads = fb.html_to_threads(html)
        self.assertEqual(len(threads), 3)
        for index, thread in enumerate(threads, start=1):
            self.assertIsInstance(thread, Tag)
            self.assertEqual(thread.text, "Thread{}".format(index))


    def test_html_to_thread_requires_string(self):
        with self.assertRaises(TypeError):
            fb.html_to_threads(100)



class ThreadToJSONTests(TestCase):

    def test_can_convert_thread_to_json(self):
        thread = BeautifulSoup("""<div class="thread">90@fbok.com, 100@fbok.com
        <div class="message"><div class="message_header">
        <span class="user">John Ronn</span>
        <span class="meta">Friday, 19 August 2016 at 13:13 UTC+01</span>
        </div></div><p>Hello?</p><div class="message">
        <div class="message_header"><span class="user">Myke</span>
        <span class="meta">Friday, 19 August 2016 at 13:15 UTC+01</span>
        </div></div><p>Hello!</p></div></div>""", "html.parser").find("div")
        json = fb.thread_to_json(thread)
        self.assertEqual(json, [{
         "text": "Hello?",
         "sender": {"name": "John Ronn", "tags": []},
         "timestamp": "2016-08-19 13:13:00"
        }, {
         "text": "Hello!",
         "sender": {"name": "Myke", "tags": []},
         "timestamp": "2016-08-19 13:15:00"
        }])


    def test_html_to_thread_requires_thread(self):
        with self.assertRaises(TypeError):
            fb.thread_to_json("<html>")
