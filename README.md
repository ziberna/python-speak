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


--------------------------------------------------------------------------------

To try it, clone the repo, then:

    $ python pythonspeak.py

__WARNING__: PythonSpeak does NOT yet provide any security against someone
entering malicious Python code. Create a new room for yourself to test it on
your own (i.e. type some random string on room input). Run in a virtual machine
if you want to be extra careful.

You can still test the project if you have only one XMPP account to play with.
Every piece of code is executed on receive. This is intended -- you get a
vague feeling when others received the message. So just type anything into the
shell. If PythonSpeak works, it will be sent to the chat room and executed when
you get the code back from the chat room.

The shell interface is currently coded with the help of backspace characters.
This is to provide dynamic prompt (which changes based on input state) and to
prevent cursor misplacement when you receive a message from another user.


--------------------------------------------------------------------------------

Requirements:

 - XMPP account (GMail, Jabber.org, et cetera)


Dependencies:

 - Python 3
 - SleekXMPP for Python 3
