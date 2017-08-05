from unittest import TestCase
from unittest.mock import Mock, patch
import pychats.parse.facebook as fb
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
