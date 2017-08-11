from datetime import datetime
import os
from unittest import TestCase
import pychats

class Tests(TestCase):

    def test_load_facebook_messages(self):
        log = pychats.from_facebook("itests/test_files/messages.htm")

        self.assertEqual(log.name(), "Facebook")
        convs = sorted(log.conversations(), key=lambda k: len(k.messages()))
        self.assertEqual(len(convs), 4)
        convs.reverse()
        conv1, conv2, conv3, conv4 = convs

        self.assertEqual(len(conv1.messages()), 6)
        self.assertEqual(conv1.messages()[0].text(), "Hello!")
        self.assertEqual(
         conv1.messages()[0].timestamp(), datetime(2014, 6, 4, 13, 22, 0)
        )
        self.assertEqual(conv1.messages()[0].sender().name(), "John Ronn")
        self.assertEqual(conv1.messages()[-1].text(), "Never mind!")

        self.assertEqual(len(conv2.messages()), 5)
        self.assertEqual(conv2.messages()[0].text(), "Hi all.")
        self.assertEqual(
         conv2.messages()[0].timestamp(), datetime(2017, 6, 8, 12, 28, 0)
        )
        self.assertEqual(conv2.messages()[0].sender().name(), "777@facebook.com")
        self.assertEqual(conv2.messages()[-1].text(), "All things pass into eternity.")
