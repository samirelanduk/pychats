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



class AttachmentContentsPropertyTests(TestCase):

    def test_attachment_contents(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap1.png")
        self.assertIs(att._contents, att.contents())


    def test_can_update_attachment_contents(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap1.png")
        att.contents(b"Non semper erit aestas")
        self.assertEqual(att._contents, b"Non semper erit aestas")


    def test_new_contents_must_be_bytes(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap1.png")
        with self.assertRaises(TypeError):
            att.contents("1000")



class AttachmentFilenamePropertyTests(TestCase):

    def test_attachment_filename(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap1.png")
        self.assertIs(att._filename, att.filename())


    def test_can_update_attachment_filename(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap1.png")
        att.filename("snap2.gif")
        self.assertEqual(att._filename, "snap2.gif")


    def test_new_filename_must_be_str(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap1.png")
        with self.assertRaises(TypeError):
            att.filename(b"1000")



class AttachmentExtensionTests(TestCase):

    def test_can_get_extension(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap.1.png")
        self.assertEqual(att.extension(), "png")


    def test_can_get_no_extension(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap")
        self.assertEqual(att.extension(), "")


    def test_can_update_extension(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap.1.png")
        att.extension("gif")
        self.assertEqual(att._filename, "snap.1.gif")


    def test_can_add_extentsion(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap")
        att.extension("gif")
        self.assertEqual(att._filename, "snap.gif")


    def test_attachment_must_be_str(self):
        att = Attachment(b"\x01\x02\x03\x04", "snap")
        with self.assertRaises(TypeError):
            att.extension(b"1000")
