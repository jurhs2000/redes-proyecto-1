from sleekxmpp import ClientXMPP

class Client(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.on_session_start)

    def on_session_start(self, event):
        self.set_status('chat', 'available')

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