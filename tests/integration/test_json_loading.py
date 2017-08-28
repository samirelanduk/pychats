from datetime import datetime
import os
import shutil
from unittest import TestCase
import pychats

class Tests(TestCase):

    def tearDown(self):
        if os.path.exists("tests/integration/test_files/temp.json"):
            os.remove("tests/integration/test_files/temp.json")
        if os.path.exists("tests/integration/test_files/attachments"):
            shutil.rmtree("tests/integration/test_files/attachments")


    def test_load_and_save(self):
        self.maxDiff = None
        log = pychats.from_json("tests/integration/test_files/log.json")

        self.assertEqual(log.name(), "Intercepted communications")
        convs = sorted(log.conversations(), key=lambda k: len(k.messages()))
        self.assertEqual(len(convs), 3)
        convs.reverse()
        conv1, conv2, conv3 = convs

        self.assertEqual(len(conv1.messages()), 6)
        self.assertEqual(conv1.messages()[0].text(), "I know this isn't ordained.")
        self.assertEqual(
         conv1.messages()[0].timestamp(), datetime(1942, 1, 24, 14, 34, 3)
        )
        self.assertEqual(conv1.messages()[0].sender().name(), "John Flonn")

        self.assertEqual(len(conv2.messages()), 4)
        self.assertEqual(conv2.messages()[0].text(), "Did they arrive?")
        self.assertEqual(
         conv2.messages()[0].timestamp(), datetime(1942, 1, 27, 14, 34, 3)
        )
        self.assertEqual(conv2.messages()[0].sender().name(), "Barry O'Darry")

        self.assertEqual(len(conv3.messages()), 3)
        self.assertEqual(conv3.messages()[0].text(), "We've lost haven't we?")
        self.assertEqual(
         conv3.messages()[0].timestamp(), datetime(1942, 9, 27, 14, 34, 3)
        )
        self.assertEqual(conv3.messages()[0].sender().name(), "John Flonn")

        people = set()
        for conv in convs:
            for message in conv.messages():
                people.add(message.sender())
        self.assertEqual(len(people), 5)
        self.assertEqual(
         set([person.name() for person in people]),
         set(["John Flonn", "Kurt Hurt", "Barry O'Darry", "Jane de la Plain", "Florence Torrence"])
        )
        john = [p for p in people if p.name() == "John Flonn"][0]
        self.assertEqual(john.tags(), set(["male", "soldier"]))

        log.save("tests/integration/test_files/temp.json")
        with open("tests/integration/test_files/temp.json") as f:
            new = f.read()
        with open("tests/integration/test_files/log.json") as f:
            old = f.read()
        self.assertEqual(new.strip(), old.strip())


    def test_load_and_save_with_attachments(self):
        log = pychats.from_json(
         "tests/integration/test_files/attachment_tests/log.json"
        )
        convs = sorted(log.conversations(), key=lambda k: len(k.messages()))
        self.assertEqual(len(convs), 3)
        convs.reverse()
        conv = convs[-1]
        message = conv.messages()[-2]
        self.assertEqual(message.text(), "Sure have.")

        attachments = message.attachments()
        self.assertEqual(len(attachments), 2)
        self.assertEqual(attachments[0].filename(), "cat1.jpg")
        self.assertEqual(attachments[1].filename(), "cat2.png")
        self.assertEqual(attachments[0].extension(), "jpg")
        self.assertEqual(attachments[1].extension(), "png")

        log.save("tests/integration/test_files/temp.json")
        with open("tests/integration/test_files/temp.json") as f:
            new = f.read()
        with open("tests/integration/test_files/attachment_tests/log.json") as f:
            old = f.read()
        self.assertEqual(new.strip(), old.strip())
        new_files = os.listdir("tests/integration/test_files/attachments")
        old_files = os.listdir(
         "tests/integration/test_files/attachment_tests/attachments"
        )
        self.assertCountEqual(new_files, old_files)
        for nf in new_files:
            with open("tests/integration/test_files/attachment_tests/attachments/" + nf, "rb") as f:
                old = f.read()
            with open("tests/integration/test_files/attachments/" + nf, "rb") as f:
                new = f.read()
            self.assertEqual(new, old)
