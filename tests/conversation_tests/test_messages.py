from datetime import datetime
from unittest import TestCase
from pychats.conversations import Message

class MessageCreationTests(TestCase):

    def test_can_create_message(self):
        message = Message("memento mori", datetime(2011, 3, 1, 12, 34, 32))
        self.assertEqual(message._text, "memento mori")
        self.assertEqual(message._timestamp, datetime(2011, 3, 1, 12, 34, 32))
