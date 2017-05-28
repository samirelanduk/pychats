from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock
from pychats.json.message_json import message_to_json
from pychats.chats.messages import Message
from pychats.chats.people import Contact

class MessageToJsonTests(TestCase):

    def test_can_make_json_from_message(self):
        contact = Mock(Contact)
        contact.name.return_value = "Justin Powers"
        message = Mock(Message)
        message.text.return_value = "message text"
        message.timestamp.return_value = datetime(2009, 5, 23, 12, 12, 1)
        message.sender.return_value = contact
        json = message_to_json(message)
        self.assertEqual(json, {
         "text": "message text",
         "timestamp": "2009-05-23 12:12:01",
         "sender": "Justin Powers"
        })


    def test_message_to_json_requires_message(self):
        with self.assertRaises(TypeError):
            message_to_json("some string")
