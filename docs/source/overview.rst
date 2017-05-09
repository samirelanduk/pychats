Overview
--------

Creating ChatLogs manually
~~~~~~~~~~~~~~~~~~~~~~~~~~

The most direct way to create pychats logs is to create the objects manually.
Ultimately modules will be added to create them by parsing external data
sources, such as Facebook message logs or iPhone backups, but for now this
minimal interface works nicely.

People
######

The first step is to create the contacts who have messages in the chatlog. This
is done with the :py:class:`.Contact` class:

  >>> import pychats
  >>> harry = pychats.Contact("Harry Potter")
  >>> ronald = pychats.Contact("Ron Weasley")
  >>> hermione = pychats.Contact("Hermione Granger")
  >>> harry.name()
  'Harry Potter'
  >>> ronald.name()
  'Ron Weasley'
  >>> hermione.name()
  'Hermione Granger'

Conversations and Messages
##########################

A chatlog is just a collection of conversations, which are themselves just a
series of messages. You create conversations with the :py:class:`.Conversation`
class:

>>> harry_conv = pychats.Conversation()
>>> ron_conv = pychats.Conversation()
>>> harry_conv
<Conversation (0 messages)>
>>> ron_conv
<Conversation (0 messages)>

You do need to pass any arguments when you create the conversation.

These are not much use without messages. These are created with the
:py:class:`.Message` class, and need text, a timestamp, and a sender:

  >>> from datetime import datetime
  >>> message1 = pychats.Message("Hi Harry", datetime(1993, 1, 5, 8, 2), hermione)
  >>> message2 = pychats.Message("Hi!", datetime(1993, 1, 5, 8, 7), harry)
  >>> harry_conv.add_message(message1)
  >>> harry_conv.add_message(message2)
  >>> harry_conv
  <Conversation (2 messages)>
  >>> harry_conv.messages()
  [<Message from Hermione Granger at 1993-01-05 08:02>, <Message from Harry Pott
  er at 1993-01-05 08:07>]
  >>> harry_conv.participants()
  {<Contact: Hermione Granger>, <Contact: Harry Potter>}

It doesn't matter what order you add messages in, they will always be ordered by
their timestamp.

ChatLogs
########

ChatLogs are created with the :py:class:`.ChatLog` class:

  >>> log = pychats.ChatLog("Hogwarts Data Breach")
  >>> log
  <'Hogwarts Data Breach' ChatLog (0 Conversations)>
  >>> log.add_conversation(harry_conv)
  >>> log
  <'Hogwarts Data Breach' ChatLog (1 Conversation)>

Once added, conversations will know what chatlog they are in:

  >>> harry_conv.chatlog()
  <'Hogwarts Data Breach' ChatLog (1 Conversation)>
