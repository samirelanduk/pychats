from unittest import TestCase
from pychats.conversations import Contact

class ContactCreationTests(TestCase):

    def test_can_create_contact(self):
        contact = Contact("Marvin Goodwright")
        self.assertEqual(contact._name, "Marvin Goodwright")


    def test_contact_name_must_be_str(self):
        with self.assertRaises(TypeError):
            Contact(111)
