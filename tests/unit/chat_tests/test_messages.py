from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch
from pychats.chats.people import Contact
from pychats.chats.messages import Message
from pychats.chats.conversations import Conversation

class MessageTest(TestCase):

    def setUp(self):
        self.contact1 = Mock(Contact)
        self.contact2 = Mock(Contact)
        self.contact3 = Mock(Contact)
        self.contact1.name.return_value = "Lafayette"
        self.conversation = Mock(Conversation)


class MessageCreationTests(MessageTest):

    def test_can_create_message(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        self.assertEqual(message._text, "memento mori")
        self.assertEqual(message._timestamp, datetime(2011, 3, 1, 12, 34, 32))
        self.assertEqual(message._sender, self.contact1)
        self.assertEqual(message._conversation, None)
        self.assertEqual(message._attachments, [])


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



class MessageFromJsonTests(TestCase):

    def test_can_make_message_with_existing_contact(self):
        contact1 = Mock(Contact)
        contact1.name.return_value = "Justin Powers"
        contact2 = Mock(Contact)
        contact2.name.return_value = "Lydia Powers"
        json = {
         "text": "message text",
         "timestamp": "2009-05-23 12:12:01",
         "sender": {"name": "Justin Powers", "tags": ["tag1", "tag2"]}
        }
        Contact.all_contacts = set([contact1, contact2])
        message = Message.from_json(json)
        self.assertEqual(message._text, "message text")
        self.assertEqual(message._timestamp, datetime(2009, 5, 23, 12, 12, 1))
        self.assertIs(message._sender, contact1)


    @patch("pychats.chats.messages.Contact.from_json")
    def test_can_make_message_with_new_contact(self, mock_contact):
        contact1 = Mock(Contact)
        contact1.name.return_value = "Justin Powers"
        contact2 = Mock(Contact)
        contact2.name.return_value = "Lydia Powers"
        contact3 = Mock(Contact)
        mock_contact.return_value = contact3
        json = {
         "text": "message text",
         "timestamp": "2009-05-23 12:12:01",
         "sender": {"name": "Marvin Powers", "tags": ["tag1", "tag2"]}
        }
        Contact.all_contacts = set([contact1, contact2])
        message = Message.from_json(json)
        mock_contact.assert_called()
        self.assertEqual(message._text, "message text")
        self.assertEqual(message._timestamp, datetime(2009, 5, 23, 12, 12, 1))
        self.assertIs(message._sender, contact3)


    def test_json_to_message_requires_dict(self):
        with self.assertRaises(TypeError):
            Message.from_json("some string")


    def test_json_to_message_requires_text_key(self):
        with self.assertRaises(ValueError):
            Message.from_json({"wrong": "txt", "timestamp": "", "sender": ""})


    def test_json_to_message_requires_timestamp_key(self):
        with self.assertRaises(ValueError):
            Message.from_json({"text": "txt", "wrong": "", "sender": ""})


    def test_json_to_message_requires_sender_key(self):
        with self.assertRaises(ValueError):
            Message.from_json({"text": "txt", "timestamp": "", "wrong": ""})



class MessageReprTests(MessageTest):

    def test_message_repr(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        self.assertEqual(
         str(message),
         "<Message from Lafayette at 2011-03-01 12:34>"
        )



class MessageEqualityTests(MessageTest):

    def test_messages_equal(self):
        message1 = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        message2 = Mock(Message)
        message2._text = "memento mori"
        message2._timestamp = datetime(2011, 3, 1, 12, 34, 32)
        message2._sender = self.contact1
        self.assertTrue(message1 == message2)
        self.assertFalse(message1 != message2)


    def test_messages_unequal(self):
        message1 = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        message2 = Mock(Message)
        message2._text = "mementomori"
        message2._timestamp = datetime(2011, 3, 1, 12, 34, 32)
        message2.sender = self.contact1
        self.assertTrue(message1 != message2)
        self.assertFalse(message1 == message2)
        message2._text = "memento mori"
        message2._timestamp = datetime(2011, 3, 1, 12, 34, 31)
        self.assertTrue(message1 != message2)
        self.assertFalse(message1 == message2)
        message2._timestamp = datetime(2011, 3, 1, 12, 34, 31)
        message2._sender = "sender"
        self.assertTrue(message1 != message2)
        self.assertFalse(message1 == message2)


    def test_message_not_equal_non_message(self):
        message1 = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        self.assertFalse(message1 == "message2")




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


    @patch("pychats.chats.conversations._sort_messages")
    def test_updating_timestamp_will_make_message_rearrange_in_conversation(self, mock_sort):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        message._conversation = Mock(Conversation)
        message._conversation._messages = [message]
        message.timestamp(datetime(2012, 1, 19, 9, 23, 56))
        mock_sort.assert_called_with([message])




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



class MessageAttachmentsTests(MessageTest):

    def test_can_get_attachments(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        message._attachments = ["a1", "a2", "a3"]
        self.assertEqual(message.attachments(), ("a1", "a2", "a3"))



class MessageConversationTests(MessageTest):

    def test_message_conversation(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        message._conversation = "A conversation"
        self.assertIs(message._conversation, message.conversation())



class MessageRecipientTests(MessageTest):

    def test_message_recipients_is_empty_when_no_conversation(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        self.assertEqual(message.recipients(), set())


    def test_message_recipients_is_conversation_participants_without_sender(self):
        message = Message(
         "memento mori", datetime(2011, 3, 1, 12, 34, 32), self.contact1
        )
        conversation = Mock(Conversation)
        conversation.participants.return_value = set(
         [self.contact1, self.contact2, self.contact3]
        )
        message._conversation = conversation
        self.assertEqual(
         message.recipients(),
         set([self.contact2, self.contact3])
        )



class MessageToJsonTests(TestCase):

    def test_can_make_json_from_message(self):
        contact = Mock(Contact)
        contact.name.return_value = "Justin Powers"
        contact.tags.return_value = set(["aaa"])
        message = Message(
         "message text", datetime(2009, 5, 23, 12, 12, 1), contact
        )
        contact.to_json.return_value = {"name": "J", "tags": ["aaa"]}
        json = message.to_json()
        contact.to_json.assert_called()
        self.assertEqual(json, {
         "text": "message text",
         "timestamp": "2009-05-23 12:12:01",
         "sender": {"name": "J", "tags": ["aaa"]}
        })
