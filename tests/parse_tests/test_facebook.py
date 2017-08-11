from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock
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
        self.assertEqual(json, {"messages": [{
         "text": "Hello?",
         "sender": {"name": "John Ronn", "tags": []},
         "timestamp": "2016-08-19 13:13:00"
        }, {
         "text": "Hello!",
         "sender": {"name": "Myke", "tags": []},
         "timestamp": "2016-08-19 13:15:00"
        }], "members": ["90@fbok.com", "100@fbok.com"]})


    def test_html_to_thread_requires_thread(self):
        with self.assertRaises(TypeError):
            fb.thread_to_json("<html>")



class ThreadConsolidationTests(TestCase):

    def test_can_consolidate_threads(self):
        threads = [
         {"messages": ["a", "b", "c"], "members": [10, 20]},
         {"messages": ["d", "e"], "members": [10, 20, 30]},
         {"messages": ["f", "g", "h"], "members": [10, 20, 30]},
         {"messages": ["i", "j", "k"], "members": [20, 50]},
         {"messages": ["l", "m"], "members": [10, 20]},
         {"messages": ["n", "o", "p"], "members": [50, 20]},
        ]
        threads = fb.consolidate_threads(threads)
        self.assertEqual(threads, [
         {"messages": ["m", "l", "c", "b", "a"]},
         {"messages": ["e", "d"]},
         {"messages": ["h", "g", "f"]},
         {"messages": ["p", "o", "n", "k", "j", "i"]},
        ])



class HtmlToChatLogTests(TestCase):

    @patch("pychats.parse.facebook.html_to_threads")
    @patch("pychats.parse.facebook.thread_to_json")
    @patch("pychats.parse.facebook.consolidate_threads")
    @patch("pychats.chats.chatlogs.ChatLog.from_json")
    def test_chatlog_creation(self, from_json, mock_con, mock_json, mock_threads):
        html = "<html>"
        thread1, thread2 = Mock(), Mock()
        mock_threads.return_value = [thread1, thread2]
        mock_json.side_effect = [["a", "b"], ["c", "d"]]
        mock_con.return_value = [["a", "b"], ["c", "d"]]
        log = Mock()
        from_json.return_value = log

        chatlog = fb.html_to_chatlog(html)

        mock_threads.assert_called_with("<html>")
        mock_json.assert_any_call(thread1)
        mock_json.assert_any_call(thread2)
        mock_con.assert_called_with([["a", "b"], ["c", "d"]])
        from_json.assert_called_with(
         {"name": "Facebook", "conversations": [["a", "b"], ["c", "d"]]}
        )
        self.assertIs(log, chatlog)



class FacebookFileLoadingTests(TestCase):

    @patch("pychats.parse.facebook.html_to_chatlog")
    @patch("builtins.open")
    def test_loading_from_json_file(self, mock_open, mock_html):
        open_return = MagicMock()
        mock_file = Mock()
        open_return.__enter__.return_value = mock_file
        mock_file.read.return_value = "<html>"
        mock_open.return_value = open_return
        mock_html.return_value = "log object"
        log = fb.from_facebook("path/to/file")
        mock_open.assert_called_with("path/to/file")
        mock_html.assert_called_with("<html>")
        self.assertEqual(log, "log object")
