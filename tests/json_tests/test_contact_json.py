from unittest import TestCase
from unittest.mock import Mock
from pychats.json.contact_json import contact_to_json
from pychats.chats.people import Contact

class ContactToJsontests(TestCase):

    def test_can_make_contact_from_json(self):
        contact = Mock(Contact)
        contact.name.return_value = "Lord Asriel"
        json = contact_to_json(contact)
        self.assertEqual(json, {"name": "Lord Asriel"})


    def test_contact_to_json_requires_contact(self):
        with self.assertRaises(TypeError):
            contact_to_json("some string")
