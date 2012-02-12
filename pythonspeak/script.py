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


import io
import sys
import codeop
import traceback
import contextlib
import readline
import re

compile = codeop.compile_command


DONE = 0
MORE = 1
ERROR = -1

BLACKLIST = (
    'os',
    'subprocess',
)

def blacklisted(string):
    pattern = '(%s)' % '|'.join(BLACKLIST)
    for match in re.finditer(pattern, string):
        start = match.start()
        end = match.end()
        if start > 0 and re.search('^[a-zA-Z0-9]$', string[start-1]):
            continue
        if end < len(string) and re.search('^[a-zA-Z0-9]$', string[end]):
            continue
        return string[start:end]
    return None


class BlacklistedError(Exception):
    def __init__(self, module):
        self.module = module
    
    def __str__(self):
        return 'This module was blacklisted: ' + self.module


class ScriptBase(object):
    """
    A shell imitator. Adds code line by line, saving it to buffer. The code
    is executed when it is possible to compile it and buffer is cleared.
    Attribute 'status' contains information about current state of input.
    
    TODO: log the script and save it to a file.
    """
    source_buffer = ''
    symbol = 'single'
    
    def __init__(self, namespace={}, file='<script>'):
        self.namespace = namespace
        self.file = file
        self.status = DONE
        namespace['BlacklistedError'] = BlacklistedError
    
    def add(self, line):
        """
        Add a line to the source buffer. Clear the buffer on successful compile.
        """
        black_module = blacklisted(line)
        if black_module is not None:
            line = 'raise BlacklistedError("%s")' % black_module
        self.source_buffer += line
        # compile
        compiled = self.compile(self.source_buffer)
        # execute and save the output
        if self.status == DONE:
            output = self.execute(compiled)
        else:
            output = ''
        # edit the buffer
        if self.status == MORE:
            self.source_buffer += '\n'
        else:
            self.source_buffer = ''
        return output
    
    def handle_compile_error(self, error):
        """
        Meant to be replaced with a custom handler.
        """
        try:
            raise error
        except (SyntaxError, OverflowError, ValueError):
            traceback.print_exc()
    
    def handle_execute_error(self, error):
        """
        Meant to be replaced with a custom handler.
        """
        try:
            raise error
        except:
            traceback.print_exc()
    
    def compile(self, source):
        """
        Compiles the given source, returns None or compiled object.
        """
        try:
            compiled = compile(source, self.file, self.symbol)
        except (SyntaxError, OverflowError, ValueError) as error:
            compiled = self.handle_compile_error(error)
            self.status = ERROR
        else:
            self.status = DONE if compiled else MORE
        return compiled
    
    def execute(self, compiled):
        """
        Executes the compiled object and returns the output.
        """
        with catch_output() as output:
            try:
                exec(compiled, self.namespace, self.namespace)
            except Exception as error:
                return self.handle_execute_error(error)
        return output.getvalue()


@contextlib.contextmanager
def catch_output():
    """
    Context manager that captures standard output and yields the result.
    """
    clipboard = sys.stdout
    output = io.StringIO()
    sys.stdout = output
    yield output
    sys.stdout = clipboard

