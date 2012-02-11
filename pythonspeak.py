#=============================================================================
# PythonSpeak, a room-chat application for Python speakers
# Copyright (C) 2012  Jure Ziberna
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#=============================================================================

#-----------------------------------------------------------------------------
# PythonSpeak is only a prototype that might never be fully developed. It is
# an experimentation.
# If you want to help turn this into a proper program:
#  - go to https://github.com/jzib/python-speak
#  - fork the repository
#  - git clone to your local machine
#  - start hacking
#  - push the code to Github
#  - submit pull request
#-----------------------------------------------------------------------------


import logging
import getpass
import random

from pythonspeak import PythonSpeak


logging.basicConfig(level=logging.ERROR, format='%(levelname)-8s %(message)s')


def main():
    print('Do you speak Python?')
    print('')
    print('You need XMPP account (Gmail, Jabber.org, et cetera).')
    
    # Get user settings
    username = input('Username*: ').strip()
    if not username:
        return
    if '@' not in username:
        username += '@jabber.org'
    
    password = getpass.getpass('Password*: ')
    
    room = input('Room: ').strip()
    if not room:
        room = 'python-speak' + str(random.randint(1000,9999))
    if '@' not in room:
        room += '@conference.jabber.org'
        
    nickname = input('Nickname: ').strip()
    if not nickname:
        nickname, _, _ = username.partition('@')
    
    # Run PythonSpeak
    python_speak = PythonSpeak(username, password, room, nickname)
    print('')
    try:
        python_speak.connect()
    except:
        python_speak.disconnect()
        raise


if __name__ == '__main__':
    main()

