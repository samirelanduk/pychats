from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch
from pychats.json.message_json import message_to_json
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
