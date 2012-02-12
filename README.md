Do you speak Python?
====================

__PythonSpeak__ is XMPP-room-based chat client with a twist -- you must speak in
Python! It works like Python's interactive shell, but everything you type is
sent to your chat room and added to the Python shell of everybody in the room.
You can write whole classes together, one line at the time. In result, you have
a pseudo-shared state of your script. __It might be best described as shared
Python shell__.

PythonSpeak is just an experiment at the moment. It _does_ work (for me at
least), but the code isn't pretty.

__NOTE__: These modules have been blacklisted:

 - os
 - subprocess

That means nobody in the chat room can use them. It does not matter if the
sender is using PythonSpeak or not, because the code is checked on receive.
BlacklistedError is raised when someone tries to use any of the blacklisted
modules.


Try it
------

Clone the repo, then:

    $ python pythonspeak.py

You can still test the project if you have only one XMPP account to play with.
Every piece of code is executed on receive. This is intended -- you get a
feeling when others received the message. So just type anything into the shell.
If PythonSpeak works, it will be sent to the chat room and executed when you get
the code back from the chat room.

The shell interface is currently coded with the help of backspace characters.
This is to provide dynamic prompt (which changes based on input state) and to
prevent cursor misplacement when you receive a message from another user.


Chat session example
---------------------

This is me having two terminals opened, where I connected to the same room with
two different XMPP accounts. The shell "conversation" looks the same on both
sides.

	[jure@Kant python-speak]$ python pythonspeak.py
	Do you speak Python?
	
	You need XMPP account (Gmail, Jabber.org, et cetera).
	Username*: j.ziberna@gmail.com
	Password*: 
	Room: python-speak2971
	Nickname: jure

	Connecting...
	Getting roster...
	Sending presence...
	Joining the room...
	Getting room configuration...
	Room already there.
	Joined room python-speak2971@conference.jabber.org.

	todd>>> # got online
	jure>>> a = 3
	todd>>> a
	3
	jure>>> def square(n):
	todd...     # this is such a cliche example
	jure...     # i know
	todd...     return n * n
	todd...
	jure>>> square(a)
	9
	todd>>> # i'm just going to import math
	jure>>> import math # first!
	todd>>> # logging out...
	jure>>> #exit

	Disconnecting...
	[jure@Kant python-speak]$ 



--------------------------------------------------------------------------------

Requirements:

 - XMPP account (Gmail, Jabber.org, et cetera)


Dependencies:

 - Python 3
 - SleekXMPP for Python 3
