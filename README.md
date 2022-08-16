
# XMPP Chat

A Python chat following the XMPP protocol, using the `Sleekxmpp` library.

## About this project

This is a schoolar project made by Julio Herrera (19402) for the course CC3067 (Redes) for the University of the Valley of Guatemala.
The server used is `alumchat.fun`.

The project has the following objectives:

 - [x]  Register an account on the server
 - [x]  Login to an existent account
 - [x]  End session
 - [x]  Remove account from the server
 - [x]  Show all users on the server
 - [x]  Add an user as a contact
 - [x]  Show details of a user doing a search
 - [x]  Receive and send messages to a contact/user
 - [x]  Create, join and send messages to rooms
 - [x]  Receive notifications
 - [ ]  Send and receive files

# How to use

This is a program using CLI, to run the program you need to install the Sleekxmpp library
```
pip install sleekxmpp
```

Once you have this requirement, execute the `main.py` file to run the program, first you will se a login menu, once you're logged in you can access to the client options.
Note: You don't need to add the `@alumchat.fun` to every user or room (only required on the email field while creating a new account).

### References
This project is based on [the Sleekxmpp documentation](https://sleekxmpp.readthedocs.io/en/latest/), the [XMPP protocols definitions](https://xmpp.org/extensions/xep-0077.xml) and the [Multi-User Chat (MUC) Bot](https://sleekxmpp.readthedocs.io/en/latest/getting_started/muc.html) Sleekxmpp's reference.
