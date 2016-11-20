from unittest import TestCase
from unittest.mock import Mock
from pychats.chats import ChatLog, Conversation

class ChatLogTest(TestCase):

    def setUp(self):
        self.conversation1 = Mock(Conversation)
        self.conversation2 = Mock(Conversation)
        self.conversation3 = Mock(Conversation)



class ChatlogCreationTests(ChatLogTest):

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



class ChatLogPropertiesTests(ChatLogTest):

    def test_chatlog_properties(self):
        chatlog = ChatLog("Facebook")
        self.assertEqual(chatlog._name, chatlog.name())
        self.assertEqual(chatlog._conversations, chatlog.conversations())


    def test_can_update_chatlog_properties(self):
        chatlog = ChatLog("Facebook")
        chatlog.name("WhatsApp")
        self.assertEqual(chatlog.name(), "WhatsApp")


    def test_chatlog_name_must_be_set_to_str(self):
        chatlog = ChatLog("Facebook")
        with self.assertRaises(TypeError):
            chatlog.name(100)


    def test_conversations_is_read_only(self):
        chatlog = ChatLog("Facebook")
        chatlog._conversations = set([self.conversation1, self.conversation2])
        self.assertEqual(len(chatlog.conversations()), 2)
        chatlog.conversations().add(self.conversation3)
        self.assertEqual(len(chatlog.conversations()), 2)


    def test_can_add_conversation(self):
        chatlog = ChatLog("Facebook")
        chatlog.add_conversation(self.conversation1)
        self.assertEqual(chatlog.conversations(), set([self.conversation1]))
        chatlog.add_conversation(self.conversation2)
        self.assertEqual(
         chatlog.conversations(),
         set([self.conversation1, self.conversation2])
        )
        chatlog.add_conversation(self.conversation3)
        self.assertEqual(
         chatlog.conversations(),
         set([self.conversation1, self.conversation2, self.conversation3])
        )


    def test_can_only_add_conversation(self):
        chatlog = ChatLog("Facebook")
        with self.assertRaises(TypeError):
            chatlog.add_conversation("Conv")


    def test_cannot_add_existing_conversation(self):
        chatlog = ChatLog("Facebook")
        chatlog.add_conversation(self.conversation1)
        with self.assertRaises(ValueError):
            chatlog.add_conversation(self.conversation1)


    def test_can_remove_conversations(self):
        chatlog = ChatLog("Facebook")
        chatlog.add_conversation(self.conversation1)
        chatlog.add_conversation(self.conversation2)
        self.assertEqual(
         chatlog.conversations(),
         set([self.conversation1, self.conversation2])
        )
        chatlog.remove_conversation(self.conversation1)
        self.assertEqual(chatlog.conversations(), set([self.conversation2]))
