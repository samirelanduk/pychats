from unittest import TestCase
from unittest.mock import Mock
from pychats.chats.conversations import Conversation
from pychats.chats.chatlogs import ChatLog

class ChatlogTest(TestCase):

    def setUp(self):
        self.conversation1 = Mock(Conversation)
        self.conversation2 = Mock(Conversation)
        self.conversation3 = Mock(Conversation)



class ChatlogCreationTests(ChatlogTest):

    def test_can_create_chatlog(self):
        chatlog = ChatLog("Facebook")
        self.assertEqual(chatlog._name, "Facebook")
        self.assertEqual(chatlog._conversations, set())


    def test_chatlog_name_must_be_str(self):
        with self.assertRaises(TypeError):
            ChatLog(1000)



class ChatlogReprTests(ChatlogTest):

    def test_chatlog_repr_no_conversations(self):
        chatlog = ChatLog("Facebook")
        self.assertEqual(str(chatlog), "<'Facebook' ChatLog (0 Conversations)>")


    def test_chatlog_repr_one_conversation(self):
        chatlog = ChatLog("Facebook")
        chatlog._conversations.add(Mock(Conversation))
        self.assertEqual(str(chatlog), "<'Facebook' ChatLog (1 Conversation)>")


    def test_chatlog_repr_multiple_conversation(self):
        chatlog = ChatLog("Facebook")
        chatlog._conversations.add(Mock(Conversation))
        chatlog._conversations.add(Mock(Conversation))
        self.assertEqual(str(chatlog), "<'Facebook' ChatLog (2 Conversations)>")
        chatlog._conversations.add(Mock(Conversation))
        self.assertEqual(str(chatlog), "<'Facebook' ChatLog (3 Conversations)>")



class ChatlogNameTests(ChatlogTest):

    def test_chatlog_name(self):
        chatlog = ChatLog("Facebook")
        self.assertIs(chatlog._name, chatlog.name())


    def test_can_update_chatlog_name(self):
        chatlog = ChatLog("Facebook")
        chatlog.name("WhatsApp")
        self.assertEqual(chatlog._name, "WhatsApp")


    def test_chatlog_name_must_be_set_to_str(self):
        chatlog = ChatLog("Facebook")
        with self.assertRaises(TypeError):
            chatlog.name(100)



class ChatLogConversationsTests(ChatlogTest):

    def test_chatlog_conversations(self):
        chatlog = ChatLog("Facebook")
        self.assertEqual(chatlog._conversations, chatlog.conversations())
        self.assertIsNot(chatlog._conversations, chatlog.conversations())



class ChatlogConversationAdditionTests(ChatlogTest):

    def test_can_add_conversation(self):
        chatlog = ChatLog("Facebook")
        chatlog.add_conversation(self.conversation1)
        self.assertEqual(chatlog._conversations, set([self.conversation1]))
        chatlog.add_conversation(self.conversation2)
        self.assertEqual(
         chatlog._conversations,
         set([self.conversation1, self.conversation2])
        )
        chatlog.add_conversation(self.conversation3)
        self.assertEqual(
         chatlog._conversations,
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



class ChatlogConversationRemovalTests(ChatlogTest):

    def test_can_remove_conversations(self):
        chatlog = ChatLog("Facebook")
        chatlog.add_conversation(self.conversation1)
        chatlog.add_conversation(self.conversation2)
        self.assertEqual(
         chatlog._conversations,
         set([self.conversation1, self.conversation2])
        )
        chatlog.remove_conversation(self.conversation1)
        self.assertEqual(chatlog._conversations, set([self.conversation2]))
