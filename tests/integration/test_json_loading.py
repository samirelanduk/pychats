from datetime import datetime
import os
from unittest import TestCase
import pychats

class Tests(TestCase):

    def tearDown(self):
        if os.path.exists("tests/integration/test_files/temp.json"):
            os.remove("tests/integration/test_files/temp.json")


    def test_load_and_save(self):
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
        self.assertEqual(new, old)
