from unittest import TestCase
from unittest.mock import Mock
from pychats.chats import ChatLog

class ChatlogCreationTests(TestCase):

    def test_can_create_chatlog(self):
        chatlog = ChatLog("Facebook")
        self.assertEqual(chatlog._name, "Facebook")
        self.assertEqual(chatlog._conversations, set())


    def test_chatlog_name_must_be_str(self):
        with self.assertRaises(TypeError):
            ChatLog(1000)


    def test_chatlog_repr(self):
        chatlog = ChatLog("Facebook")
        self.assertEqual(str(chatlog), "<'Facebook' ChatLog (0 Conversations)>")



class ChatLogPropertiesTests(TestCase):

    def test_chatlog_properties(self):
        chatlog = ChatLog("Facebook")
        self.assertIs(chatlog._name, chatlog.name())
        self.assertIs(chatlog._conversations, chatlog.conversations())
