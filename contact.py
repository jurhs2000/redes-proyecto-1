class Contact():
    def __init__(self, jid, Email=None, Username=None, Name=None):
        self.jid = jid
        self.Email = Email
        self.Username = Username
        self.Name = Name
        self.messages = []

    def set_info(self, key, value):
        self.__setattr__(key, value)

    # receive a contact and update the no None fields
    def update(self, contact):
        for key in contact.__dict__.keys():
            if contact.__getattribute__(key) != None:
                self.__setattr__(key, contact.__getattribute__(key))
        return self

    def add_message(self, message):
        self.messages.append(message)

    def __str__(self) -> str:
        # print all the fields of the contact
        return str(self.__dict__)