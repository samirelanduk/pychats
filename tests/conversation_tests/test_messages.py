from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock
from pychats.conversations import Message, Contact

class MessageTest(TestCase):

    def setUp(self):
        self.contact = Mock(Contact)
        self.contact.name.return_value = "Lafayette"


class MessageCreationTests(MessageTest):

    def test_can_create_message(self):
        message = Message(
         "memento mori",
         datetime(2011, 3, 1, 12, 34, 32),
         self.contact
        )
        self.assertEqual(message._text, "memento mori")
        self.assertEqual(message._timestamp, datetime(2011, 3, 1, 12, 34, 32))
        self.assertEqual(message._sender, self.contact)


    def test_message_repr(self):
        message = Message(
         "memento mori",
         datetime(2011, 3, 1, 12, 34, 32),
         self.contact
        )
        self.assertEqual(
         str(message),
         "<Message from Lafayette at 2011-03-01 12:34>"
        )
