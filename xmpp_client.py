from sleekxmpp import ClientXMPP
from sleekxmpp.xmlstream.stanzabase import ET
from sleekxmpp.exceptions import IqTimeout, IqError
from sleekxmpp.plugins.xep_0004.stanza.form import Form
from sleekxmpp.plugins.xep_0004.stanza.field import FormField, FieldOption

from contact import Contact


class Client(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.on_session_start)
        self.contacts = []

    def on_session_start(self, event):
        self.set_status('chat', 'available')
        self.update_roster()

    def update_roster(self):
        roster = self.get_roster()
        print(roster)
        for jid in roster['roster']['items'].keys():
            contact = Contact(jid)
            for k, v in roster['roster']['items'][jid].items():
                print(k, v)
                contact.set_roster_info(k, v)
            self.contacts.append(contact)

    def send_message_to_user(self, jid, message):
        print(jid, message)
        self.send_message(mto=jid, mbody=message, mtype='chat')

    def login(self):
        if self.connect(("alumchat.fun", 5222), use_ssl=False, use_tls=False):
            self.process()
            return True
        return False

    def set_status(self, show, status):
        self.send_presence(pshow=show, pstatus=status)

    def get_all_contacts(self):
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
            value='*'
        )
        query = ET.Element('{jabber:iq:search}query')
        query.append(form.xml)
        iq.append(query)
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
                            users.append(Contact(jid=values['jid'], Email=values['Email'], Username=values['Username'], Name=values['Name']))
        except IqError as e:
            print(e.iq)
        except IqTimeout:
            print('Tiempo de espera agotado')
        for user in users:
            print(user)
        return users

    def create_iq(self, **kwargs):
        iq = self.Iq()
        iq.set_from(self.boundjid.full)
        for k, v in kwargs.items():
            iq[k] = v
        return iq
