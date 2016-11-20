from unittest import TestCase
from unittest.mock import Mock
from pychats.chats import ChatLog

class ChatlogCreationTests(TestCase):

    def test_can_create_chatlog(self):
        chatlog = ChatLog("Facebook")
        self.assertEqual(chatlog._name, "Facebook")
        self.assertEqual(chatlog._conversations, set())
