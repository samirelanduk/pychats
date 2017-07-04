from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock, patch
from pychats.chats.conversations import Conversation, _sort_messages
from pychats.chats.people import Contact
from pychats.chats.messages import Message

class ConversationTest(TestCase):

    def setUp(self):
        self.senders = [Mock(Contact) for _ in range(5)]
        self.messages = [Mock(Message) for _ in range(5)]
        for index, message in enumerate(self.messages):
            message.timestamp.return_value = datetime(2009, 5, index + 1, 12)
            message.sender.return_value = self.senders[index % 3]
            message._conversation = None



class ConversationCreationTests(ConversationTest):

    def test_can_create_conversation(self):
        conversation = Conversation()
        self.assertEqual(conversation._messages, [])
        self.assertEqual(conversation._chatlog, None)



class ConversationFromJsonTests(TestCase):

    @patch("pychats.chats.conversations.Message.from_json")
    def test_can_create_conversation_from_json(self, mock_message):
        message1, message2, message3 = Mock(), Mock(), Mock()
        mock_message.side_effect = [message1, message2, message3]
        json = {
         "messages": ["message1", "message2", "message3"]
        }
        conversation = Conversation.from_json(json)
        mock_message.assert_any_call("message1")
        mock_message.assert_any_call("message2")
        mock_message.assert_any_call("message3")
        self.assertIsInstance(conversation, Conversation)
        self.assertEqual(conversation._messages, [message1, message2, message3])


    def test_json_to_conversation_requires_dict(self):
        with self.assertRaises(TypeError):
            Conversation.from_json("some string")


    def test_json_to_message_requires_messages_key(self):
        with self.assertRaises(ValueError):
            Conversation.from_json({"wrong": []})



class ConversationReprTests(ConversationTest):

    def test_conversation_repr_no_messages(self):
        conversation = Conversation()
        self.assertEqual(str(conversation), "<Conversation (0 messages)>")


    def test_conversation_repr_one_message(self):
        conversation = Conversation()
        conversation._messages.append(Mock(Message))
        self.assertEqual(str(conversation), "<Conversation (1 message)>")


    def test_conversation_repr_multiple_message(self):
        conversation = Conversation()
        conversation._messages.append(Mock(Message))
        conversation._messages.append(Mock(Message))
        self.assertEqual(str(conversation), "<Conversation (2 messages)>")
        conversation._messages.append(Mock(Message))
        self.assertEqual(str(conversation), "<Conversation (3 messages)>")



class ConversationMessagesTests(ConversationTest):

    def test_messages_returns_messages(self):
        conversation = Conversation()
        for message in self.messages:
            conversation._messages.append(message)
        self.assertEqual(conversation._messages, conversation.messages())
        self.assertIsNot(conversation._messages, conversation.messages())



class ConversationMessageAdditionTests(ConversationTest):

    def test_can_add_messages_to_conversation(self):
        conversation = Conversation()
        conversation.add_message(self.messages[0])
        self.assertEqual(conversation._messages, [self.messages[0]])
        conversation.add_message(self.messages[1])
        self.assertEqual(conversation._messages, self.messages[0:2])


    def test_can_only_add_messages_to_conversations(self):
        conversation = Conversation()
        with self.assertRaises(TypeError):
            conversation.add_message("Some message")


    def test_cannot_add_message_if_it_is_already_present(self):
        conversation = Conversation()
        conversation.add_message(self.messages[0])
        with self.assertRaises(ValueError):
            conversation.add_message(self.messages[0])


    def test_adding_messages_updates_conversation_of_messages(self):
        conversation = Conversation()
        self.assertIs(self.messages[0]._conversation, None)
        conversation.add_message(self.messages[0])
        self.assertIs(self.messages[0]._conversation, conversation)


    def test_adding_messages_will_order_them_by_date(self):
        conversation = Conversation()
        conversation.add_message(self.messages[2])
        self.assertEqual(conversation._messages, [self.messages[2]])
        conversation.add_message(self.messages[1])
        self.assertEqual(conversation._messages, self.messages[1:3])
        conversation.add_message(self.messages[0])
        self.assertEqual(conversation._messages, self.messages[:3])
        conversation.add_message(self.messages[4])
        self.assertEqual(conversation._messages, self.messages[:3] + [self.messages[-1]])
        conversation.add_message(self.messages[3])
        self.assertEqual(conversation._messages, self.messages)



class ConversationMessageRemovalTests(ConversationTest):

    def test_can_remove_messages(self):
        conversation = Conversation()
        for message in self.messages:
            conversation.add_message(message)
        conversation.remove_message(self.messages[-1])
        self.assertEqual(conversation._messages, self.messages[:-1])
        conversation.remove_message(self.messages[0])
        self.assertEqual(conversation._messages, self.messages[1:-1])
        conversation.remove_message(self.messages[2])
        self.assertEqual(
         conversation._messages,
         [self.messages[1], self.messages[3]]
        )


    def test_removing_messages_resets_message_conversation_to_none(self):
        conversation = Conversation()
        conversation.add_message(self.messages[0])
        self.assertIs(self.messages[0]._conversation, conversation)
        conversation.remove_message(self.messages[0])
        self.assertIs(self.messages[0]._conversation, None)



class ConversationChatlogTests(ConversationTest):

    def test_can_access_chatlog(self):
        conversation = Conversation()
        chatlog = "..."
        conversation._chatlog = chatlog
        self.assertIs(conversation.chatlog(), chatlog)



class ConversationParticipantTests(ConversationTest):

    def test_can_get_conversation_participants(self):
        conversation = Conversation()
        self.assertEqual(conversation.participants(), set())
        conversation.add_message(self.messages[0])
        self.assertEqual(
         conversation.participants(),
         set([self.senders[0]])
        )
        conversation.add_message(self.messages[1])
        self.assertEqual(
         conversation.participants(),
         set(self.senders[0:2])
        )
        conversation.add_message(self.messages[2])
        self.assertEqual(
         conversation.participants(),
         set(self.senders[0:3])
        )
        conversation.add_message(self.messages[3])
        self.assertEqual(
         conversation.participants(),
         set(self.senders[0:3])
        )
        conversation.add_message(self.messages[4])
        self.assertEqual(
         conversation.participants(),
         set(self.senders[0:3])
        )



class SortMessagesTests(ConversationTest):

    def test_can_sort_messages(self):
        messages = self.messages[2:5][::-1] + self.messages[:2]
        self.assertEqual(_sort_messages(messages), self.messages)



class ConversationToJsonTests(ConversationTest):

    def test_can_get_json_from_conversation(self):
        self.messages[0].to_json.return_value = {"aa": "bb"}
        self.messages[1].to_json.return_value = {"cc": "dd"}
        conversation = Conversation()
        conversation._messages = self.messages[:2]
        self.assertEqual(
         conversation.to_json(), {"messages": [{"aa": "bb"}, {"cc": "dd"}]}
        )
