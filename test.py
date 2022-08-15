import logging
from sleekxmpp import ClientXMPP
#import asyncio
#import sys
#if sys.platform == 'win32':
#    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Client(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler('session_start', self.on_session_start)
        
        # Register plug-ins
        '''self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer'''

        #import ssl
        #ssl._create_default_https_context = ssl._create_unverified_context
        #self.ssl_version = ssl.PROTOCOL_SSLv23

    def on_session_start(self, event):
        self.set_status('chat', 'available')

    def send_message_to_user(self, jid, message):
        print(jid, message)
        self.send_message(mto=jid, mbody=message, mtype='chat')

    def login(self):
        print(self.requested_jid)
        print(self.password)
        print(self.boundjid)
        print(self.dns_service)
        if self.connect(("alumchat.fun", 5222), use_ssl=False, use_tls=False):
            self.process()
            return True
        return False

    def set_status(self, show, status):
        self.send_presence(pshow=show, pstatus=status)

logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

client = Client('jurhs@alumchat.fun', '91vGs55@hHjJ')
if client.login():
    print('Conectado')
else:
    print('Ha ocurrido un error')
    exit()

option = ""

while option != "3":
    option = input("ingrese una opcion: ")
    if option == "1":
        client.set_status('chat', 'available')
    elif option == "2":
        client.send_message_to_user("hola@alumchat.fun", "q onda")
    elif option == "3":
        print('Saliendo')
        exit()
