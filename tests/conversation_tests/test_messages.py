from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock
from pychats.chats import Message, Contact

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


    def test_text_must_be_str(self):
        with self.assertRaises(TypeError):
            message = Message(
             100,
             datetime(2011, 3, 1, 12, 34, 32),
             self.contact
            )


    def test_timestamp_must_be_datetime(self):
        with self.assertRaises(TypeError):
            message = Message(
             "100",
             datetime(2011, 3, 1).date(),
             self.contact
            )


    def test_sender_must_be_contact(self):
        with self.assertRaises(TypeError):
            message = Message(
             "100",
             datetime(2011, 3, 1, 12, 34, 32),
             "person"
            )


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



class MessagePropertyTests(MessageTest):

    def test_can_access_message_properties(self):
        message = Message(
         "memento mori",
         datetime(2011, 3, 1, 12, 34, 32),
         self.contact
        )
        self.assertIs(message._text, message.text())
        self.assertIs(message._timestamp, message.timestamp())
        self.assertIs(message._sender, message.sender())


    def test_can_update_message_properties(self):
        message = Message(
         "memento mori",
         datetime(2011, 3, 1, 12, 34, 32),
         self.contact
        )
        message.text("Non semper erit aestas")
        message.timestamp(datetime(2012, 1, 19, 9, 23, 56))
        new_sender = Mock(Contact)
        message.sender(new_sender)
        self.assertEqual(message.text(), "Non semper erit aestas")
        self.assertEqual(message.timestamp(), datetime(2012, 1, 19, 9, 23, 56))
        self.assertIs(message.sender(), new_sender)
