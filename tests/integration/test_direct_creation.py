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
        picture_message = pychats.Message(
         "Check out these!" * 69, datetime(2009, 5, 23, 21, 2, 2), mildred
        )
        attachment1 = pychats.Attachment(b"\x01\x02\x03\x04", "snap1.png")
        attachment1 = pychats.Attachment(b"\xA1\xA2\xA3\xA4", "snap2.png")
        picture_message.add_attachment(attachment1)
        picture_message.add_attachment(attachment2)
        conversation3.add_message(picture_message)

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

        picture_message = conversation3.messages()[-1]
        self.assertEqual(len(picture_message.attachments()), 2)
        self.assertEqual(
         picture_message.attachments()[0].filename(), "snap1.png"
        )
        self.assertEqual(picture_message.attachments()[0].extension(), "png")
        self.assertEqual(
         picture_message.attachments()[0].contents(), b"\x01\x02\x03\x04"
        )


    def test_can_merge_conversations(self):
        shae = pychats.Contact("Shae")
        emma = pychats.Contact("Emma")
        drake = pychats.Contact("Drake")

        conversation1 = pychats.Conversation()
        conversation2 = pychats.Conversation()
        conversation3 = pychats.Conversation()
        conversation4 = pychats.Conversation()

        conversation1.add_message(pychats.Message(
         "Hello all!", datetime(2009, 6, 23, 12, 0, 0), drake
        ))
        conversation1.add_message(pychats.Message(
         "Hi", datetime(2009, 6, 23, 12, 1, 3), shae
        ))
        conversation1.add_message(pychats.Message(
         "Hello :)", datetime(2009, 6, 23, 12, 1, 12), emma
        ))

        conversation2.add_message(pychats.Message(
         "Hello :)", datetime(2009, 6, 23, 12, 1, 12), emma
        ))
        conversation2.add_message(pychats.Message(
         "Is there an update?", datetime(2009, 6, 23, 13, 1, 12), drake
        ))

        conversation3.add_message(pychats.Message(
         "what's up?", datetime(2009, 6, 23, 13, 1, 12), shae
        ))
        conversation3.add_message(pychats.Message(
         "Not yet!", datetime(2009, 6, 23, 13, 1, 48), emma
        ))

        conversation4.add_message(pychats.Message(
         "Hi", datetime(2009, 6, 12, 12, 0, 0), emma
        ))
        conversation4.add_message(pychats.Message(
         "Hello all!", datetime(2009, 6, 23, 12, 0, 0), drake
        ))

        merged = pychats.Conversation.merge(
         conversation1, conversation2, conversation3, conversation4
        )

        self.assertEqual(len(merged.messages()), 7)
        self.assertEqual(merged.messages()[0].text(), "Hi")
        self.assertEqual(merged.messages()[1].text(), "Hello all!")
        self.assertEqual(merged.messages()[2].text(), "Hi")
        self.assertEqual(merged.messages()[3].text(), "Hello :)")
        self.assertEqual(merged.messages()[4].text(), "Is there an update?")
        self.assertEqual(merged.messages()[5].text(), "what's up?")
        self.assertEqual(merged.messages()[6].text(), "Not yet!")
