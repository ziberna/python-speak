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


import sleekxmpp
import threading


class SpeakBase(object):
    """
    Wrapper for chat API.
    """
    def __init__(self, username, password, room, nickname):
        # Not inherited because core methods would be overwritten
        self.xmpp = sleekxmpp.ClientXMPP(username, password)
        # Settings
        self.username = username
        self.nickname = nickname
        self.room = room
        # Prepare XMPP object
        self.xmpp_add_event_handlers()
        self.xmpp_register_plugins()
    
    def xmpp_add_event_handlers(self):
        """
        Adds necessary event handlers to the XMPP object.
        """
        self.xmpp.add_event_handler('session_start', self.xmpp_session_start)
        self.xmpp.add_event_handler('muc::%s::message' % self.room, self.xmpp_receive)
        self.xmpp.add_event_handler('muc::%s::got_online' % self.room, self.xmpp_new_presence)
    
    def xmpp_register_plugins(self):
        """
        Registers/enables necessary plug-ins.
        """
        self.xmpp.register_plugin('xep_0030') # Service Discovery
        self.xmpp.register_plugin('xep_0045') # MUC (Multi-User-Chat)
        self.xmpp.register_plugin('xep_0004') # Data forms (for MUC rooms)
        self.xmpp.register_plugin('xep_0199') # Ping
    
    def connect(self):
        """
        Connects to the server. Returns True on success.
        """
        print('Connecting...')
        success = self.xmpp.connect()
        if success:
            self.xmpp.process(block=False)
        return success
    
    def disconnect(self):
        """
        Disconnects from the server.
        TODO: delete the room if there's no other presence.
        """
        print('')
        print('Disconnecting...')
        #if am_the_only_one:
        #    self.xmpp.plugin['xep_0045'].destroy(self.room)
        self.xmpp.disconnect(wait=True)
    
    def xmpp_session_start(self, event):
        """
        Does all the necessary session things, then call the join-room method.
        """
        print('Getting roster...')
        # Note: buddy list saved to self.xmpp.client_roster
        self.xmpp.get_roster()
        print('Sending presence...')
        self.xmpp.send_presence()
        self.xmpp_join_room(event)
    
    def xmpp_join_room(self, event):
        """
        Joins the room.
        TODO: manage joining better. Learn the API and XMPP protocol.
        """
        print('Joining the room...')
        self.xmpp.plugin['xep_0045'].joinMUC(self.room, self.nickname, wait=True)
        try:
            # Configure the room and apply the configuration
            print('Getting room configuration...')
            config = self.xmpp.plugin['xep_0045'].getRoomConfig(self.room)
            print('Setting room configuration...')
            self.xmpp.plugin['xep_0045'].setRoomConfig(self.room, config)
        except ValueError as error:
            # room configuration failed because room already exists (probably). join again
            print('Room already there.')
            self.xmpp.plugin['xep_0045'].joinMUC(self.room, self.nickname, wait=True)
        print('Joined room %s.' % self.room)
        self.xmpp_start()
    
    def xmpp_start(self):
        """
        Run start method in a separate thread.
        """
        thread = threading.Thread(target=self.start)
        print('')
        thread.start()
    
    def start(self):
        """
        PythonSpeak overrides this method. Called when joined the room. 
        """
        raise NotImplementedError('2+2=5 and start is not implemented.')
    
    def xmpp_receive(self, message):
        """
        Parses the message and passes it to self.receive.
        """
        nickname = message['mucnick']
        body = self.xmpp_unpack_message(message['body'])
        self.receive(body, nickname)
    
    def receive(self, body, nickname):
        """
        PythonSpeak overrides this method. Called when message is received.
        """
        raise NotImplementedError('2+2=5 and receive is not implemented.')
    
    def send(self, message):
        """
        PythonSpeak calls this method. Sends a given message to the room.
        """
        message = self.xmpp_pack_message(message)
        self.xmpp.send_message(mto=self.room, mbody=message, mtype='groupchat')
    
    def xmpp_new_presence(self, presence):
        """
        Prints a comment in the name of a person that got online.
        """
        nickname = presence['muc']['nick']
        if nickname and nickname != self.nickname:
            self.receive('# got online', nickname)
    
    def xmpp_pack_message(self, message):
        """
        SleekXMPP or XMPP itself strips the string of any trailing whitespace,
        so it's necessary to put a header string in front of the message.
        OH, any you wouldn't want someone random sending you code.
        """
        return '#pycode:' + message
    
    def xmpp_unpack_message(self, message):
        """
        Remove the header from the message. See method xmpp_pack_message.
        """
        _, _, message = message.partition('#pycode:')
        return message

