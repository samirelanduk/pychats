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



class ConversationMessagesTests(TestCase):

    def setUp(self):
        self.senders = [Mock(Contact) for _ in range(3)]
        self.messages = [Mock(Message) for _ in range(3)]
        self.conversation = Conversation()


    def test_can_add_messages_to_conversation(self):
        self.conversation.add_message(self.messages[0])
        self.assertEqual(self.conversation._messages, [self.messages[0]])
        self.conversation.add_message(self.messages[1])
        self.assertEqual(self.conversation._messages, self.messages[0:2])
