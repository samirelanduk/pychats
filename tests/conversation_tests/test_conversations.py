from unittest import TestCase
from pychats.chats import Conversation

class ConversationCreationTests(TestCase):

    def test_can_create_conversation(self):
        conversation = Conversation()
        self.assertEqual(conversation._messages, [])


    def test_conversation_repr(self):
        conversation = Conversation()
        self.assertEqual(str(conversation), "<Conversation (0 messages)>")
