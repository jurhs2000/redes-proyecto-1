from sleekxmpp import ClientXMPP
from sleekxmpp.xmlstream.stanzabase import ET
from sleekxmpp.exceptions import IqTimeout, IqError
from sleekxmpp.plugins.xep_0004.stanza.form import Form
from sleekxmpp.plugins.xep_0004.stanza.field import FormField, FieldOption

from contact import Contact

SERVER = '@alumchat.fun'
PORT = 5222

class Client(ClientXMPP):
    def __init__(self, jid, password, Name=None, Email=None):
        ClientXMPP.__init__(self, jid, password)
        self.password = password
        self.Name = Name
        self.Email = Email
        self.add_event_handler('session_start', self.on_session_start)
        self.add_event_handler("register", self.on_register)
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data forms
        self.register_plugin('xep_0066')  # Out-of-band Data
        self.register_plugin('xep_0077')  # In-band Registration
        self['xep_0077'].force_registration = True
        self.contacts = []

    def on_session_start(self, event):
        self.set_status('chat', 'available')
        self.update_roster()

    def update_roster(self):
        roster = self.get_roster()
        for jid in roster['roster']['items'].keys():
            contact = Contact(jid)
            for k, v in roster['roster']['items'][jid].items():
                contact.set_info(k, v)
            self.contacts.append(contact)

    def send_message_to_user(self, jid, message):
        self.send_message(mto=jid+SERVER, mbody=message, mtype='chat')

    def login(self):
        if self.connect((SERVER[1:], PORT), use_ssl=False, use_tls=False):
            self.process()
            return True
        return False

    def set_status(self, show, status):
        self.send_presence(pshow=show, pstatus=status)

    def add_contact(self, jid, subscription_meessage):
        self.send_presence(
            pto=jid + SERVER, pstatus=subscription_meessage, ptype="subscribe")

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
                    if connected_roster.items():
                        for _, state in connected_roster.items():
                            for k, v in state.items():
                                contact.set_info(k, v)
                    contacts.append(contact)
        print("\nContactos:")
        for contact in contacts:
            print(contact)
        return contacts

    def search_user(self, jid):
        self.update_contacts(self.get_contact_by_jid(jid))
        self.update_contacts(self.get_contacts(jid))

    def create_iq(self, **kwargs):
        iq = self.Iq()
        iq.set_from(self.boundjid.full)
        for k, v in kwargs.items():
            iq[k] = v
        return iq

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

    def update_contacts(self, contacts):
        for contact in self.contacts:
            for new_contact in contacts:
                if contact.jid == new_contact.jid:
                    contact.update(new_contact)
                    break

    def on_register(self, event):
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
