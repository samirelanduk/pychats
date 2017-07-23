pychats
=======

pychats is a library for modelling text conversations.

Example
-------

  >>> import pychats
  >>> from datetime import datetime
  >>> conversation = pychats.Conversation()
  >>> bob = pychats.Contact("Bob Loblaw")
  >>> message = pychats.Message("Hello!", datetime(1990, 9, 28, 15, 30), bob)
  conversation.add_message(message)
  >>> conversation.participants()
  {<Contact: Bob Loblaw>}




Installing
----------

pip
~~~

pychats can be installed using pip:

``$ pip3 install pychats``

pychats is written for Python 3, and does not support Python 2.

If you get permission errors, try using ``sudo``:

``$ sudo pip3 install pychats``


Development
~~~~~~~~~~~

The repository for pychats, containing the most recent iteration, can be
found `here <http://github.com/samirelanduk/pychats/>`_. To clone the
pychats repository directly from there, use:

``$ git clone git://github.com/samirelanduk/pychats.git``


Requirements
~~~~~~~~~~~~

pychats currently has no external dependencies, and is pure Python.


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
is done with the ``Contact`` class:

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

You can give these people 'tags' to categorise them:

  >>> harry.add_tag("wizard")
  >>> harry.add_tag("gryffindor")
  >>> harry.tags()
  {'wizard', 'gryffindor'}


Conversations and Messages
##########################

A chatlog is just a collection of conversations, which are themselves just a
series of messages. You create conversations with the ``Conversation``
class:

>>> harry_conv = pychats.Conversation()
>>> ron_conv = pychats.Conversation()
>>> harry_conv
<Conversation (0 messages)>
>>> ron_conv
<Conversation (0 messages)>

You do need to pass any arguments when you create the conversation.

These are not much use without messages. These are created with the
``Message`` class, and need text, a timestamp, and a sender:

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

ChatLogs are created with the ``ChatLog`` class:

  >>> log = pychats.ChatLog("Hogwarts Data Breach")
  >>> log
  <'Hogwarts Data Breach' ChatLog (0 Conversations)>
  >>> log.add_conversation(harry_conv)
  >>> log
  <'Hogwarts Data Breach' ChatLog (1 Conversation)>

Once added, conversations will know what chatlog they are in:

  >>> harry_conv.chatlog()
  <'Hogwarts Data Breach' ChatLog (1 Conversation)>


Storing ChatLogs as JSON
~~~~~~~~~~~~~~~~~~~~~~~~

ChatLogs have a ``ChatLog.save`` method which will save the while
structure to file as JSON. You can call ``from_json`` to recreate
the structure.

  >>> log.save("backup.json")
  >>> recovered_log = pychats.from_json("backup.json")

Contacts, Messages, Conversations and ChatLogs all have ``to_json`` methods and
``from_json`` alternative constructors to individually convert them to and from
JSON if needed.

  >>> message1.to_json()
  {'text': 'Hi!', 'timestamp': '1993-01-05 08:07:00', 'sender': {'name': 'Harry
  Potter', 'tags': []}}


Changelog
---------

Release 2.1.0
~~~~~~~~~~~~~

`23 July 2017`

* Added JSON input and output.
* Gave Contact objects tags.


Release 2.0.0
~~~~~~~~~~~~~

`9 May 2017`

* Added the basic conversation classes for manual creation of chatlogs.
