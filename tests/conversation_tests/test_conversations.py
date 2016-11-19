from unittest import TestCase
from pychats.chats import Conversation

class ConversationCreationTests(TestCase):

    def test_can_create_conversation(self):
        conversation = Conversation()
        self.assertEqual(conversation._messages, [])
