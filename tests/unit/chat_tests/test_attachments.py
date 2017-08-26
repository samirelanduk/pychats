from unittest import TestCase
from pychats.chats.messages import Attachment

class AttachmentCreationTests(TestCase):

    def test_can_create_attachment(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap1.png")
        self.assertEqual(att._contents, b"\x01\x02\x03\x04")
        self.assertEqual(att._filename, "snap1.png")


    def test_contents_must_be_bytes(self):
        with self.assertRaises(TypeError):
            Attachment("sss", "snap1.png")


    def test_filename_must_be_str(self):
        with self.assertRaises(TypeError):
            Attachment(b"sss", b"snap1.png")



class AttachmentReprTests(TestCase):

    def test_attachment_repr(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap1.png")
        self.assertEqual(str(att), "<Attachment 'snap1.png' (4 bytes)>")
