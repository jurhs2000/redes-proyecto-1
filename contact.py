class Contact():
    def __init__(self, jid, Email, Username, Name):
        self.jid = jid
        self.Email = Email
        self.Username = Username
        self.Name = Name

    def set_roster_info(self, key, value):
        self.__setattr__(key, value)

    def __str__(self) -> str:
        return self.jid