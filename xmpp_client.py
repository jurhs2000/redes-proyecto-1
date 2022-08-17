import base64
from sleekxmpp import ClientXMPP
from sleekxmpp.xmlstream.stanzabase import ET
from sleekxmpp.exceptions import IqTimeout, IqError
from sleekxmpp.plugins.xep_0004.stanza.form import Form
from contact import Contact

SERVER = '@alumchat.fun'
ROOM_SERVER = '@conference.alumchat.fun'
PORT = 5222

'''# Uncomment to see debug messages
import logging
logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')'''

class Client(ClientXMPP):
    def __init__(self, jid, password, Name=None, Email=None, registering=False):
        ClientXMPP.__init__(self, jid, password)
        self.password = password
        self.Name = Name
        self.Email = Email
        self.registering = registering # True if client was created for registration, False if client was created for login
        self.to_chat = False # Indicates if the client is waiting for a response to a message
        self.contacts = []
        self.rooms = {}
        self.add_event_handler('session_start', self.on_session_start)
        self.add_event_handler("register", self.on_register)
        self.add_event_handler("presence_subscribe", self.on_presence_subscribe)
        self.add_event_handler("presence_unsubscribe", self.on_presence_unsubscribe)
        self.add_event_handler("got_offline", self.on_got_offline)
        self.add_event_handler("got_online", self.on_got_online)
        self.add_event_handler("message", self.on_message)
        self.add_event_handler("changed_status", self.on_changed_status)
        self.add_event_handler("groupchat_invite", self.muc_invite)
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0065') # SOCKS5 Bytestreams
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0071') # XHTML-IM
        self.register_plugin('xep_0077') # In-band Registration
        self['xep_0077'].force_registration = True
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0096') # File transfer
        self.register_plugin('xep_0231') # BOB

    def on_session_start(self, event):
        self.set_status('chat', 'available')
        self.update_roster()

    def on_message(self, msg):
        show_response = True
        # For messages received from a groupchat
        if msg['type'] == 'groupchat':
            # get the nick
            nick = msg['mucnick']
            # If you sent the message, don't show the notification
            if nick == self.boundjid.user:
                show_response = False
            # For other's messages, show the notification
            else:
                # get the room
                room = msg['from'].bare.split('@')[0]
                # get the message
                message = msg['body']
                print(f'\n[{room}] {nick}: {message}')
                # add the message to the room chat history
                self.rooms[room].append(f'[{room}] {nick}: {message}')
                self.to_chat_type = 'room'
                self.message_receiver = room
        # For messages received from an user
        else:
            # remove all after @
            user = msg['from'].bare.split('@')[0]
            # If you sent the message, don't show the notification
            if user == self.boundjid.user:
                show_response = False
            # For other's messages, show the notification
            else:
                print(f'\n{user}: {msg["body"]}')
                # add the message to the chat history
                for contact in self.contacts:
                    if contact.jid == user:
                        contact.add_message(f'{user}: {msg["body"]}')
                        self.to_chat_type = 'contact'
                        self.message_receiver = user
                        break
        if show_response:
            print("Desea responder a este mensaje? (Y/n)")
            self.to_chat = True

    # Shows the chat history of a contact
    def show_chat(self, jid):
        for contact in self.contacts:
            if contact.jid == jid:
                for message in contact.messages:
                    print(message)
                break

    # Shows the chat history of a room
    def show_room_chat(self, room):
        if room in self.rooms.keys():
            for message in self.rooms[room]:
                print(message)
        else:
            print('No estas en esta sala!')

    # Shows a notification and updates the contact when someones gets offline
    def on_got_offline(self, presence):        
        if self.boundjid.bare not in str(presence['from']):
            u = self.jid_to_user(str(presence['from']))
            print(f'{u} se desconectó')
            for i in self.contacts:
                if i.jid == str(presence['from']):
                    self.contacts.remove(i)
                    break

    # Shows a notification and updates the contact when someones gets online
    def on_got_online(self, presence):
        if self.boundjid.bare not in str(presence['from']):
            u = self.jid_to_user(str(presence['from']))
            print(f'{u} se conectó')
            for i in self.contacts:
                if i.jid == str(presence['from']):
                    i.online = True
                    break

    # Get the roster (contacts list) and updates the contacts list
    def update_roster(self):
        roster = self.get_roster()
        contacts_roster = []
        for jid in roster['roster']['items'].keys():
            contact = Contact(jid)
            for k, v in roster['roster']['items'][jid].items():
                contact.set_info(k, v)
            contacts_roster.append(contact)
        self.update_contacts(contacts_roster)

    # Send message and updates the chat history of the contact
    def send_message_to_user(self, jid, message):
        self.send_message(mto=jid+SERVER, mbody=message, mtype='chat')
        for contact in self.contacts:
            if contact.jid == jid:
                contact.add_message("{}: {}".format("You:", message))
                break

    # Not implemented
    async def send_file_to_user(self, jid, file):
        '''m = self.Message()
        m['to'] = jid+SERVER
        m['type'] = 'chat'
        with open(file, 'rb') as img_file:
            img = img_file.read()
        if img:
            cid = self['xep_0231'].set_bob(img, 'image/png')
            m['body'] = 'Tried sending an image using HTML-IM + BOB'
            m['html']['body'] = '<img src="cid:%s" />' % cid
            m.send()'''
        '''with open(file, 'rb') as img:
            file = base64.b64encode(img.read()).decode('utf-8')

        self.send_message(mto=jid+SERVER, mbody=file, mtype='chat')'''
        try:
            self.file = open(file, 'rb')
            # Open the S5B stream in which to write to.
            proxy = await self['xep_0065'].handshake(jid+SERVER)

            # Send the entire file.
            while True:
                data = self.file.read(1048576)
                if not data:
                    break
                await proxy.write(data)

            # And finally close the stream.
            proxy.transport.write_eof()
        except (IqError, IqTimeout):
            print('File transfer errored')
        else:
            print('File transfer finished')
        finally:
            self.file.close()

    # Show notification when someone added you as a contact
    def on_presence_subscribe(self, presence):
        username = presence['from'].bare
        print(f'{username} quiere agregarte a tu lista de contactos')

    # Show notification when someone removed you from the contact list
    def on_presence_unsubscribe(self, presence):
        username = presence['from'].bare
        print(f'{username} te ha eliminado de su lista de contactos')

    # Show notification when someone change his status
    def on_changed_status(self, presence):
        username = presence['from'].bare
        print(self.client_roster.presence[username]['status'])
        print(f'{username} ha cambiado su estado a {self.client_roster.presence[username]["status"]}')

    # Connect to the server, used on login and register
    def login(self):
        if self.connect((SERVER[1:], PORT), use_ssl=False, use_tls=False):
            self.process()
            return True
        return False

    # Set a new presence status and message
    def set_status(self, show, status):
        self.send_presence(pshow=show, pstatus=status)

    # Add a new contact to the contact list if it doesn't exist
    def add_contact(self, jid, subscription_meessage):
        for contact in self.contacts:
            if contact.jid == jid:
                print('Este contacto ya existe')
            else:
                contact.add_message(subscription_meessage)
                self.send_presence(
                    pto=jid + SERVER, pstatus=subscription_meessage, ptype="subscribe")

    # show all the users in the server or show users that match the jid
    def get_contacts(self, jid='*'):
        iq = self.get_search_iq(jid)
        users = []
        try:
            search_result = iq.send()
            search_result = ET.fromstring(str(search_result))
            for query in search_result:
                for x in query:
                    for item in x:
                        values = {}
                        for field in list(item):
                            for value in list(field):
                                values[field.attrib['var']] = value.text
                        if values != {}:
                            users.append(Contact(
                                jid=values['jid'], Email=values['Email'], Username=values['Username'], Name=values['Name']))
        except IqError as e:
            print(e.iq)
        except IqTimeout:
            print('Tiempo de espera agotado')
        print("\nUsuarios en el servidor:")
        for user in users:
            print(user)
        return users

    # Get the roster (contacts list) and search for contacts that match the jid
    def get_contact_by_jid(self, jid):
        self.update_roster()
        groups = self.client_roster.groups()
        contacts = []
        for group in groups:
            for user in groups[group]:
                contact = Contact(jid=user)
                # if user string icludes jid
                if user.find(jid) != -1:
                    user_roster = self.client_roster[user]
                    contact.set_info('Name', user_roster['name'])
                    contact.set_info(
                        'Subscription', user_roster['subscription'])
                    contact.set_info('Groups', user_roster['groups'])
                    connected_roster = self.client_roster.presence(user)
                    # Presence info set (show, status)
                    if connected_roster.items():
                        for _, state in connected_roster.items():
                            for k, v in state.items():
                                contact.set_info(k, v)
                    contacts.append(contact)
        print("\nContactos:")
        for contact in contacts:
            print(contact)
        return contacts

    # Search in the contact list and in the server
    def search_user(self, jid):
        self.update_contacts(self.get_contact_by_jid(jid))
        self.get_contacts(jid)

    # Creates an Iq with the specific attributes
    def create_iq(self, **kwargs):
        iq = self.Iq()
        iq.set_from(self.boundjid.full)
        for k, v in kwargs.items():
            iq[k] = v
        return iq

    # Custom Iq for search users
    def get_search_iq(self, search_value='*'):
        iq = self.create_iq(type="set", id="search_result",
                            to="search." + self.boundjid.domain)
        form = Form()
        form.set_type("submit")
        form.add_field(
            var='FORM_TYPE',
            type='hidden',
            value='jabber:iq:search'
        )
        form.add_field(
            var='Username',
            type='boolean',
            value=1
        )
        form.add_field(
            var='search',
            type='text-single',
            value=search_value
        )
        query = ET.Element('{jabber:iq:search}query')
        query.append(form.xml)
        iq.append(query)
        return iq

    # Receive a new list of contacts and update the self.contacts list, adding new contacts and updating existing ones.
    def update_contacts(self, contacts):
        for contact in self.contacts:
            for new_contact in contacts:
                if contact.jid == new_contact.jid:
                    contact.update(new_contact)
                    break
                else:
                    self.contacts.append(new_contact)

    # Register a new user in the server
    def on_register(self, event):
        if self.registering:
            iq = self.Iq()
            iq['type'] = 'set'
            iq['register']['username'] = self.boundjid.user
            iq['register']['password'] = self.password
            iq['register']['name'] = self.Name
            iq['register']['email'] = self.Email
            try:
                iq.send(now=True)
            except IqError as e:
                print(e.iq)
            except IqTimeout:
                print('Tiempo de espera agotado')

    # Create a room specifying the name, affiliation and configuring the room
    def create_group(self, room):
        self.plugin['xep_0045'].joinMUC(room+ROOM_SERVER, self.boundjid.user, wait=True)
        self.plugin['xep_0045'].setAffiliation(room+ROOM_SERVER, self.boundjid.full, affiliation='owner')
        self.plugin['xep_0045'].configureRoom(room+ROOM_SERVER, ifrom=self.boundjid.full)
        self.rooms[room] = []

    # Join a room by name
    def join_group(self, room):
        self.plugin['xep_0045'].joinMUC(room+ROOM_SERVER, self.boundjid.user)
        self.rooms[room] = []
        self.add_event_handler("muc::%s::got_online" % room+ROOM_SERVER, self.muc_online)

    # Send message to a room and updates the room chat history
    def send_message_to_group(self, room, message):
        if room in self.rooms.keys():
            self.send_message(mto=room+ROOM_SERVER, mbody=message, mtype='groupchat')
            self.rooms[room].append(f'[{room}] {self.boundjid.user}: {message}')

    # Show notification when someone joins the room and updates the room chat history
    def muc_online(self, presence):
        # If user joined is not the current user
        if presence['muc']['nick'] != self.boundjid.user:
            print(f'{presence["muc"]["nick"]} se ha conectado a la sala')
            self.rooms[presence['muc']['room']].append(f'{presence["muc"]["nick"]} se ha conectado a la sala')

    # Show notification when someone invites you to a room
    def muc_invite(self, inv):
        print('invitacion a grupo')

    # Remove a contact from your contact list
    def delete_contact(self, jid):
        self.del_roster_item(jid+SERVER)
        for contact in self.contacts:
            if contact.jid == jid:
                self.contacts.remove(contact)
                break

    # Remove your account from the server
    def delete_account(self):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['from'] = self.boundjid.bare
        iq['register']['remove'] = True
        try:
            result = iq.send()
            if result['type'] == 'result':
                print('Cuenta eliminada')
                self.disconnect()
        except IqError as e:
            print(e.iq)
            self.disconnect()
        except IqTimeout:
            print('Tiempo de espera agotado')
            self.disconnect()
