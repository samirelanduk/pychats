from unittest import TestCase
from unittest.mock import Mock, patch
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



class ChatlogFromJsonTests(TestCase):

    @patch("pychats.chats.chatlogs.Conversation.from_json")
    def test_can_create_conversation_from_json(self, mock_conversation):
        conv1, conv2, conv3 = Mock(), Mock(), Mock()
        mock_conversation.side_effect = [conv1, conv2, conv3]
        json = {
         "name": "Log Name",
         "conversations": ["conv1", "conv2", "conv3"]
        }
        log = ChatLog.from_json(json)
        mock_conversation.assert_any_call("conv1")
        mock_conversation.assert_any_call("conv2")
        mock_conversation.assert_any_call("conv3")
        self.assertIsInstance(log, ChatLog)
        self.assertEqual(log._name, "Log Name")
        self.assertEqual(log._conversations, [conv1, conv2, conv3])


    def test_json_to_chatlog_requires_dict(self):
        with self.assertRaises(TypeError):
            ChatLog.from_json("some string")


    def test_json_to_chatlog_requires_name_key(self):
        with self.assertRaises(ValueError):
            ChatLog.from_json({"wrong": "name"})


    def test_json_to_chatlog_requires_conversations_key(self):
        with self.assertRaises(ValueError):
            ChatLog.from_json({"wrong": []})



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


    def test_adding_conversation_updates_its_chatlog(self):
        chatlog = ChatLog("Facebook")
        chatlog.add_conversation(self.conversation1)
        self.assertEqual(self.conversation1._chatlog, chatlog)



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
