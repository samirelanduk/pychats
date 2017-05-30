from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch
from pychats.json.message_json import message_to_json, json_to_message
from pychats.chats.messages import Message
from pychats.chats.people import Contact

class MessageToJsonTests(TestCase):

    @patch("pychats.json.message_json.contact_to_json")
    def test_can_make_json_from_message(self, mock_contact):
        contact = Mock(Contact)
        contact.name.return_value = "Justin Powers"
        message = Mock(Message)
        message.text.return_value = "message text"
        message.timestamp.return_value = datetime(2009, 5, 23, 12, 12, 1)
        message.sender.return_value = contact
        mock_contact.return_value = {"name": "J"}
        json = message_to_json(message)
        self.assertEqual(json, {
         "text": "message text",
         "timestamp": "2009-05-23 12:12:01",
         "sender": {"name": "J"}
        })
        mock_contact.assert_called_with(contact)


    def test_message_to_json_requires_message(self):
        with self.assertRaises(TypeError):
            message_to_json("some string")



class JsonToMessageTests(TestCase):

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
        message = json_to_message(json, [contact1, contact2])
        self.assertEqual(message._text, "message text")
        self.assertEqual(message._timestamp, datetime(2009, 5, 23, 12, 12, 1))
        self.assertIs(message._sender, contact1)


    @patch("pychats.json.message_json.json_to_contact")
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
        message = json_to_message(json, [contact1, contact2])
        self.assertEqual(message._text, "message text")
        self.assertEqual(message._timestamp, datetime(2009, 5, 23, 12, 12, 1))
        self.assertIs(message._sender, contact3)
        mock_contact.assert_called_with(json["sender"])


    def test_json_to_message_requires_dict(self):
        with self.assertRaises(TypeError):
            json_to_message("some string")


    def test_json_to_message_requires_text_key(self):
        with self.assertRaises(ValueError):
            json_to_message({"wrong": "txt", "timestamp": "", "sender": ""}, [])


    def test_json_to_message_requires_timestamp_key(self):
        with self.assertRaises(ValueError):
            json_to_message({"text": "txt", "wrong": "", "sender": ""}, [])


    def test_json_to_message_requires_sender_key(self):
        with self.assertRaises(ValueError):
            json_to_message({"text": "txt", "timestamp": "", "wrong": ""}, [])


    def test_json_to_message_needs_contacts(self):
        with self.assertRaises(TypeError):
            json_to_message({"text": "", "timestamp": "", "sender": ""}, ["s"])
