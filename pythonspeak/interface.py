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


class Interface(object):
    """
    The most complex UI in the whole universe (trademark).
    
    JOKING!
    
    TODO: start cursing at curses or use a profanity framework (e.g. urwid).
    Curses is preferred (means less dependencies for users).
    
    Potential issue with using curses - printing output instantly.
    Example problem:
        for n in range(3):
            print('displayed afterwards')
            time.sleep(1)
    When capturing output instead of letting it display, the whole piece of
    code has to execute first. The solution is to redirect output to a curses
    widget of sorts (a text box).
    """
    
    buffer = ''
    
    def write(self, string):
        self.buffer += string
    
    def writeln(self, string):
        self.buffer += string + '\n'
    
    def delete(self, length=0):
        self.buffer += '\b' * length
    
    def refresh(self):
        print(self.buffer, end='')
        self.flush()
    
    def flush(self):
        self.buffer = ''

