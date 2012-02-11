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


import traceback

import pythonspeak.speak as speak
import pythonspeak.script as script
import pythonspeak.interface as interface


class PythonScript(script.ScriptBase):
    """
    Extends ScriptBase. See pythonspeak.script module.
    """
    def handle_execute_error(self, error):
        """
        Returns traceback of a given error.
        TODO: make this code less stupid.
        """
        try:
            raise error
        except:
            return traceback.format_exc()
    
    def get_prompt(self):
        """
        Returns appropriate prompt string.
        """
        if self.status == script.MORE:
            return '... '
        else:
            return '>>> '


class PythonSpeak(speak.SpeakBase):
    """
    Extends chat API wrapper.
    """
    def __init__(self, *args, **kwargs):
        super(PythonSpeak, self).__init__(*args, **kwargs)
        self.script = PythonScript()
    
    def start(self):
        """
        Starts the PythonSpeak shell.
        """
        # set flags
        self.running = True
        self.receiving = False
        # input (main) loop
        while self.running:
            # wait if receiving
            try:
                while self.receiving:
                    pass
            except KeyboardInterrupt:
                print('')
                break
            # get the current prompt
            prompt = self.nickname[:4] + self.script.get_prompt()
            # input the code line
            try:
                message = input(prompt)
            except EOFError:
                print('')
                break
            except KeyboardInterrupt as error:
                print(error)
            # check for exit
            if message in ('#exit', '#quit'):
                message = '# logging out...'
                self.send(message)
                self.running = False
            else:
                # send the message
                self.send(message)
                # set receiving to true
                self.receiving = True
        self.disconnect()
    
    def receive(self, message, nickname):
        """
        Handles a received message (executes and prints output).
        There are some hacks needed with the prompt. It doesn't work nicely
        when user has received a message while having typed something.
        
        See pythonspeak/interface.py.
        """
        # lock
        self.receiving = True
        ui = interface.Interface()
        if nickname == self.nickname:
            # get the output
            output = self.script.add(message)
            # add the output
            ui.write(output)
            # refresh the interface
            ui.refresh()
        else:
            # delete the current prompt
            ui.delete(8)
            # add sender's prompt
            ui.write(nickname[:4] + self.script.get_prompt())
            # add sender's message
            ui.writeln(message)
            # execute sender's message, to get the new prompt and the output
            output = self.script.add(message)
            # add the output
            ui.write(output)
            # add the new prompt
            ui.write(self.nickname[:4] + self.script.get_prompt())
            # refresh the interface
            ui.refresh()
        # unlock
        self.receiving = False

