from datetime import datetime
from unittest import TestCase
import pychats

class Tests(TestCase):

    def test_load_and_save(self):
        log = pychats.from_json("itests/test_files/log.json")

        self.assertEqual(log.name(), "Intercepted communications")
        convs = sorted(log.conversations(), key=lambda k: len(k.messages()))
        self.assertEqual(len(convs), 3)
