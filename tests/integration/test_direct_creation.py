from datetime import datetime
from unittest import TestCase
import pychats

class Tests(TestCase):

    def test_can_make_chatlog(self):
        marvin = pychats.Contact("Marvin Goodwright")
        mildred = pychats.Contact("Mildred Mayhew")

        conversation1 = pychats.Conversation()
        conversation1.add_message(pychats.Message(
         "Hello Marvin", datetime(2009, 5, 23, 12, 0, 0), mildred
        ))
        conversation1.add_message(pychats.Message(
         "Hello Mildred", datetime(2009, 5, 23, 12, 0, 12), marvin
        ))
        conversation1.add_message(pychats.Message(
         "I enjoyed this interaction", datetime(2009, 5, 23, 12, 1, 4), mildred
        ))
        conversation1.add_message(pychats.Message(
         "As did I.", datetime(2009, 5, 23, 12, 1, 56), marvin
        ))

        spencer = pychats.Contact("Spencer Splendidboots")

        conversation2 = pychats.Conversation()
        conversation2.add_message(pychats.Message(
         "Mildred is being weird.", datetime(2009, 5, 23, 12, 5, 21), marvin
        ))
        conversation2.add_message(pychats.Message(
         "Mildred is always weird.", datetime(2009, 5, 23, 12, 5, 10), spencer
        ))
        conversation2.add_message(pychats.Message(
         "Tru dat.", datetime(2009, 5, 23, 12, 5, 59), marvin
        ))

        conversation3 = pychats.Conversation()
        conversation3.add_message(pychats.Message(
         "Hi guys!", datetime(2009, 5, 23, 19, 45, 2), mildred
        ))
        conversation3.add_message(pychats.Message(
         "Hello Mildred...", datetime(2009, 5, 23, 19, 45, 14), spencer
        ))
        conversation3.add_message(pychats.Message(
         "Yes. Hello.", datetime(2009, 5, 23, 19, 46, 4), marvin
        ))
        conversation3.add_message(pychats.Message(
         "lol" * 69, datetime(2009, 5, 23, 19, 48, 2), mildred
        ))

        chatlog = pychats.ChatLog("Test chatlog")
        chatlog.add_conversation(conversation1)
        chatlog.add_conversation(conversation2)
        chatlog.add_conversation(conversation3)

        self.assertEqual(chatlog.name(), "Test chatlog")
        chatlog.name("Test Chatlog")
        self.assertEqual(chatlog.name(), "Test Chatlog")

        self.assertEqual(
         chatlog.conversations(),
         set([conversation1, conversation2, conversation3])
        )

        for conversation in chatlog.conversations():
            self.assertIs(conversation.chatlog(), chatlog)


        self.assertEqual(conversation1.participants(), set([mildred, marvin]))
        self.assertEqual(conversation2.participants(), set([marvin, spencer]))
        self.assertEqual(conversation3.participants(), set([mildred, spencer, marvin]))

        for conversation in chatlog.conversations():
            for message in conversation.messages():
                self.assertIs(message.conversation(), conversation)


        last_message = conversation1.messages()[-1]
        last_message.timestamp(datetime(1990, 1, 1, 12, 30, 12))
        self.assertEqual(conversation1.messages()[0], last_message)
