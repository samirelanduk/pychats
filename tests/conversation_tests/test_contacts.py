from unittest import TestCase
from pychats.chats.people import Contact

class ContactCreationTests(TestCase):

    def test_can_create_contact(self):
        contact = Contact("Marvin Goodwright")
        self.assertEqual(contact._name, "Marvin Goodwright")


    def test_contact_name_must_be_str(self):
        with self.assertRaises(TypeError):
            Contact(111)



class ContactReprTests(TestCase):

    def test_contacts_repr(self):
        contact = Contact("Marvin Goodwright")
        self.assertEqual(str(contact), "<Contact: Marvin Goodwright>")



class ContactNameTests(TestCase):

    def test_contact_name_property(self):
        contact = Contact("Marvin Goodwright")
        self.assertIs(contact._name, contact.name())


    def test_can_modify_contact_name(self):
        contact = Contact("Marvin Goodwright")
        contact.name("Albus Dumbledore")
        self.assertEqual(contact._name, "Albus Dumbledore")


    def test_can_only_set_contact_name_to_str(self):
        contact = Contact("Marvin Goodwright")
        with self.assertRaises(TypeError):
            contact.name(123)
