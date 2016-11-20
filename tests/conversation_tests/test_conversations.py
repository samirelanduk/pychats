from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock
from pychats.chats import Conversation, Contact, Message

class ConversationCreationTests(TestCase):

    def test_can_create_conversation(self):
        conversation = Conversation()
        self.assertEqual(conversation._messages, [])


    def test_conversation_repr(self):
        conversation = Conversation()
        self.assertEqual(str(conversation), "<Conversation (0 messages)>")
        conversation._messages.append(Mock(Message))
        self.assertEqual(str(conversation), "<Conversation (1 message)>")
        conversation._messages.append(Mock(Message))
        self.assertEqual(str(conversation), "<Conversation (2 messages)>")
        conversation._messages.append(Mock(Message))
        self.assertEqual(str(conversation), "<Conversation (3 messages)>")



class ConversationMessagesTests(TestCase):

    def setUp(self):
        self.senders = [Mock(Contact) for _ in range(5)]
        self.messages = [Mock(Message) for _ in range(5)]
        for index, message in enumerate(self.messages):
            message.timestamp.return_value = datetime(2009, 5, index + 1, 12)
            message._conversation = None
        self.conversation = Conversation()


    def test_can_add_messages_to_conversation(self):
        self.conversation.add_message(self.messages[0])
        self.assertEqual(self.conversation._messages, [self.messages[0]])
        self.conversation.add_message(self.messages[1])
        self.assertEqual(self.conversation._messages, self.messages[0:2])


    def test_can_only_add_messages_to_conversations(self):
        with self.assertRaises(TypeError):
            self.conversation.add_message("Some message")


    def test_cannot_add_message_if_it_is_already_present(self):
        self.conversation.add_message(self.messages[0])
        with self.assertRaises(ValueError):
            self.conversation.add_message(self.messages[0])


    def test_adding_messages_updates_conversation_of_messages(self):
        self.assertIs(self.messages[0]._conversation, None)
        self.conversation.add_message(self.messages[0])
        self.assertIs(self.messages[0]._conversation, self.conversation)


    def test_can_access_messages(self):
        self.conversation.add_message(self.messages[0])
        self.assertEqual(
         self.conversation.messages(),
         self.conversation._messages
        )


    def test_message_access_is_read_only(self):
        self.conversation.add_message(self.messages[0])
        self.assertEqual(self.conversation._messages, [self.messages[0]])
        self.conversation.messages().append(self.messages[1])
        self.assertEqual(self.conversation._messages, [self.messages[0]])


    def test_adding_messages_will_order_them_by_date(self):
        self.conversation.add_message(self.messages[2])
        self.assertEqual(self.conversation._messages, [self.messages[2]])
        self.conversation.add_message(self.messages[1])
        self.assertEqual(self.conversation._messages, self.messages[1:3])
        self.conversation.add_message(self.messages[0])
        self.assertEqual(self.conversation._messages, self.messages[:3])
        self.conversation.add_message(self.messages[4])
        self.assertEqual(self.conversation._messages, self.messages[:3] + [self.messages[-1]])
        self.conversation.add_message(self.messages[3])
        self.assertEqual(self.conversation._messages, self.messages)


    def test_can_remove_messages(self):
        for message in self.messages:
            self.conversation.add_message(message)
        self.conversation.remove_message(self.messages[-1])
        self.assertEqual(self.conversation._messages, self.messages[:-1])
        self.conversation.remove_message(self.messages[0])
        self.assertEqual(self.conversation._messages, self.messages[1:-1])
        self.conversation.remove_message(self.messages[2])
        self.assertEqual(
         self.conversation._messages,
         [self.messages[1], self.messages[3]]
        )
