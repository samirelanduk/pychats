from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock
from pychats.chats import Message, Contact, Conversation

class MessageTest(TestCase):

    def setUp(self):
        self.contact1 = Mock(Contact)
        self.contact2 = Mock(Contact)
        self.contact3 = Mock(Contact)
        self.contact1.name.return_value = "Lafayette"


class MessageCreationTests(MessageTest):

    def test_can_create_message(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        self.assertEqual(message._text, "memento mori")
        self.assertEqual(message._timestamp, datetime(2011, 3, 1, 12, 34, 32))
        self.assertEqual(message._sender, self.contact1)
        self.assertEqual(message._conversation, None)


    def test_text_must_be_str(self):
        with self.assertRaises(TypeError):
            message = Message(
             100, datetime(2011, 3, 1, 12, 34, 32), self.contact1
            )


    def test_timestamp_must_be_datetime(self):
        with self.assertRaises(TypeError):
            message = Message(
             "memento", datetime(2011, 3, 1, 12, 34, 32).date(), self.contact1
            )


    def test_sender_must_be_contact(self):
        with self.assertRaises(TypeError):
            message = Message(
             "memento mori", datetime(2011, 3, 1, 12, 34, 32), "person"
            )



class MessageReprTests(MessageTest):

    def test_message_repr(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        self.assertEqual(
         str(message),
         "<Message from Lafayette at 2011-03-01 12:34>"
        )



class MessageTextTests(MessageTest):

    def test_message_text(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        self.assertIs(message._text, message.text())


    def test_can_update_message_text(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        message.text("Non semper erit aestas")
        self.assertEqual(message._text, "Non semper erit aestas")


    def test_new_text_must_be_str(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        with self.assertRaises(TypeError):
            message.text(1000)



class MessageTimestampTests(MessageTest):

    def test_message_timestamp(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        self.assertIs(message._timestamp, message.timestamp())


    def test_can_update_message_timestamp(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        message.timestamp(datetime(2012, 1, 19, 9, 23, 56))
        self.assertEqual(message._timestamp, datetime(2012, 1, 19, 9, 23, 56))


    def test_new_timestamp_must_be_datetime(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        with self.assertRaises(TypeError):
            message.timestamp(1000)
        with self.assertRaises(TypeError):
            message.timestamp(datetime(2012, 1, 19, 9, 23, 56).date())



class MessageSenderTests(MessageTest):

    def test_message_sender(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        self.assertIs(message._sender, message.sender())


    def test_can_update_message_sender(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        message.sender(self.contact2)
        self.assertEqual(message._sender, self.contact2)


    def test_new_sender_must_be_contact(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        with self.assertRaises(TypeError):
            message.sender(1000)



class MessageConversationTests(MessageTest):

    def test_message_conversation(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        message._conversation = "A conversation"
        self.assertEqual(message._conversation, message.conversation())


'''







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
        conversation.add_message(message)
        self.assertEqual(
         conversation.messages(),
         [message1, message2, message]
        )
        message.timestamp(datetime(2011, 3, 1, 12, 0, 0))
        self.assertEqual(
         conversation.messages(),
         [message1, message2, message]
        )
        message.timestamp(datetime(2011, 3, 1, 11, 0, 0))
        self.assertEqual(
         conversation.messages(),
         [message1, message, message2]
        )
        message.timestamp(datetime(2011, 3, 1, 10, 0, 0))
        self.assertEqual(
         conversation.messages(),
         [message, message1, message2]
        )



    def test_message_recipients_is_empty_when_no_conversation(self):
        self.assertEqual(message.recipients(), set())


    def test_can_get_message_recipients_from_conversation(self):
        conversation = Mock(Conversation)
        conversation.participants.return_value = set(
         [self.contact, self.contact2, self.contact3]
        )
        message._conversation = conversation
        self.assertEqual(
         message.recipients(),
         set([self.contact2, self.contact3])
        )'''
