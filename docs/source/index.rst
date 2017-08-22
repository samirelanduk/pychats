pychats
=======

pychats is a library for modelling text conversations and extracting them from
external sources, like Facebook.

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


Table of Contents
-----------------

.. toctree ::

    installing
    overview
    api
    changelog
