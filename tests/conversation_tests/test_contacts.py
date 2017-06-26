from unittest import TestCase
from pychats.chats.people import Contact

class ContactCreationTests(TestCase):

    def test_can_create_contact(self):
        contact = Contact("Marvin Goodwright")
        self.assertEqual(contact._name, "Marvin Goodwright")
        self.assertEqual(contact._tags, set())


    def test_contact_name_must_be_str(self):
        with self.assertRaises(TypeError):
            Contact(111)



class ContactFromJsonTests(TestCase):

    def test_can_make_contact_from_json(self):
        json = {"name": "Lord Asriel", "tags": ["aaa", "ddd", "zzz"]}
        contact = Contact.from_json(json)
        self.assertIsInstance(contact, Contact)
        self.assertEqual(contact._name, "Lord Asriel")
        self.assertEqual(contact._tags, set(["aaa", "ddd", "zzz"]))


    def test_contact_from_json_requires_dict(self):
        with self.assertRaises(TypeError):
            Contact.from_json("some string")


    def test_contact_from_json_requires_name_key(self):
        with self.assertRaises(ValueError):
            Contact.from_json({"wrongkey": "Lord Asriel", "tags": []})


    def test_contact_from_json_requires_tags_key(self):
        with self.assertRaises(ValueError):
            Contact.from_json({"wrongkey": [], "name": "Asriel"})



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



class ContactTagsTests(TestCase):

    def test_can_get_tags(self):
        contact = Contact("Marvin Goodwright")
        contact._tags = set(["aaa", "bbb"])
        self.assertEqual(contact._tags, contact.tags())
        self.assertIsNot(contact._tags, contact.tags())



class ContactTagAdditionTests(TestCase):

    def test_can_add_tags(self):
        contact = Contact("Marvin Goodwright")
        contact.add_tag("111")
        self.assertEqual(contact._tags, set(["111"]))
        contact.add_tag("222")
        self.assertEqual(contact._tags, set(["111", "222"]))


    def test_tags_must_be_str(self):
        contact = Contact("Marvin Goodwright")
        with self.assertRaises(TypeError):
            contact.add_tag(100)



class ContactTagRemovalTests(TestCase):

    def test_can_removal_tags(self):
        contact = Contact("Marvin Goodwright")
        contact._tags = set(["aaa", "bbb"])
        contact.remove_tag("aaa")
        self.assertEqual(contact._tags, set(["bbb"]))



class ContactToJsonTests(TestCase):

    def test_can_make_json_from_contact(self):
        contact = Contact("Lord Asriel")
        contact._tags = set()
        json = contact.to_json()
        self.assertEqual(json, {"name": "Lord Asriel", "tags": []})


    def test_can_make_tags_json_from_contact(self):
        contact = Contact("Lord Asriel")
        contact._tags = set(["aaa"])
        json = contact.to_json()
        self.assertEqual(json, {
         "name": "Lord Asriel", "tags": ["aaa"]
        })


    def test_tags_json_is_ordered(self):
        contact = Contact("Lord Asriel")
        contact._tags = set(["ddd", "zzz", "aaa"])
        json = contact.to_json()
        self.assertEqual(json, {
         "name": "Lord Asriel", "tags": ["aaa", "ddd", "zzz"]
        })
