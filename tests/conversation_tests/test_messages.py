from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock
from pychats.chats import Message, Contact, Conversation

class MessageTest(TestCase):

    def setUp(self):
        self.contact = Mock(Contact)
        self.contact2 = Mock(Contact)
        self.contact3 = Mock(Contact)
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
        self.assertEqual(message._conversation, None)


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

    def setUp(self):
        MessageTest.setUp(self)
        self.message = Message(
         "memento mori",
         datetime(2011, 3, 1, 12, 34, 32),
         self.contact
        )


    def test_can_access_message_properties(self):
        self.assertIs(self.message._text, self.message.text())
        self.assertIs(self.message._timestamp, self.message.timestamp())
        self.assertIs(self.message._sender, self.message.sender())
        self.assertIs(self.message._conversation, self.message.conversation())


    def test_can_update_message_properties(self):
        self.message.text("Non semper erit aestas")
        self.message.timestamp(datetime(2012, 1, 19, 9, 23, 56))
        new_sender = Mock(Contact)
        self.message.sender(new_sender)
        self.assertEqual(self.message.text(), "Non semper erit aestas")
        self.assertEqual(self.message.timestamp(), datetime(2012, 1, 19, 9, 23, 56))
        self.assertIs(self.message.sender(), new_sender)


    def test_new_text_must_be_str(self):
        with self.assertRaises(TypeError):
            self.message.text(1000)


    def test_new_timestamp_must_be_datetime(self):
        with self.assertRaises(TypeError):
            self.message.timestamp(1000)
        with self.assertRaises(TypeError):
            self.message.timestamp(datetime(2012, 1, 19, 9, 23, 56).date())


    def test_updating_timestamp_will_make_message_rearrange_in_conversation(self):
        conversation = Conversation()
        message1 = Message(
         "memento mori",
         datetime(2011, 3, 1, 10, 34, 32),
         self.contact
        )
        message2 = Message(
         "memento mori",
         datetime(2011, 3, 1, 11, 34, 32),
         self.contact
        )
        conversation.add_message(message1)
        conversation.add_message(message2)
        conversation.add_message(self.message)
        self.assertEqual(
         conversation.messages(),
         [message1, message2, self.message]
        )
        self.message.timestamp(datetime(2011, 3, 1, 12, 0, 0))
        self.assertEqual(
         conversation.messages(),
         [message1, message2, self.message]
        )
        self.message.timestamp(datetime(2011, 3, 1, 11, 0, 0))
        self.assertEqual(
         conversation.messages(),
         [message1, self.message, message2]
        )
        self.message.timestamp(datetime(2011, 3, 1, 10, 0, 0))
        self.assertEqual(
         conversation.messages(),
         [self.message, message1, message2]
        )


    def test_new_sender_must_be_contact(self):
        with self.assertRaises(TypeError):
            self.message.sender(1000)


    def test_message_recipients_is_empty_when_no_conversation(self):
        self.assertEqual(self.message.recipients(), set())


    def test_can_get_message_recipients_from_conversation(self):
        conversation = Mock(Conversation)
        conversation.participants.return_value = set(
         [self.contact, self.contact2, self.contact3]
        )
        self.message._conversation = conversation
        self.assertEqual(
         self.message.recipients(),
         set([self.contact2, self.contact3])
        )
