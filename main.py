'''
Universidad del Valle de Guatemala
Redes - CC3067 - Seccion 20
Catedratico: Jorge Yass
Autores: Julio Herrera - 19402
Proyecto 1 - Protocolo XMPP
'''

from xmpp_client import Client

SERVER = '@alumchat.fun'

is_authenticated = False

menu_login = '''
1. Iniciar sesion
2. Registrar nueva cuenta
3. Salir
'''

menu = '''
1. Mostrar usuarios conectados
2. Agregar usuario
3. Mostrar detalles de usuario
4. Enviar mensaje a un usuario
5. Crear grupo
6. Unirse a grupo
7. Enviar mensaje a grupo
8. Enviar mensaje de presencia
9. Eliminar contacto
10. Eliminar mi cuenta del servidor
11. Salir
'''

def get_show_precence(value):
    if value == "1":
        return "available"
    elif value == "2":
        return "away"
    elif value == "3":
        return "xa"
    elif value == "4":
        return "dnd"
    else:
        return "available"

login_option = ""
client = None

while login_option != "3":
    is_authenticated = False # Reset the authentication flag on logout
    print(menu_login)
    login_option = input("Seleccione una opcion: ")
    # Login
    if login_option == "1":
        username = input("\nIngrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")
        # TODO: Remove this hardcoded password for username
        if username == 'jurhs':
            password = "91vGs55@hHjJ"
        client = Client(username + SERVER, password)
        print("\nIniciando sesion...")
        if client.login():
            is_authenticated = True
            print("\nSesion iniciada")
        else:
            print("\nError al iniciar sesion")
    # Register
    elif login_option == "2":
        username = input("\nIngrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")
        name = input("Ingrese su nombre: ")
        email = input("Ingrese su correo: ")
        client = Client(username + SERVER, password, name, email, registering=True)
        if client.login():
            is_authenticated = True
            print("\nCuenta creada")
        else:
            print("\nError al registrar")
    elif login_option == "3":
        print("Saliendo...")
    else:
        print("Opcion no valida")

    # Main menu for authenticated users
    if is_authenticated:
        option = ""
        while option != "11":
            print(menu)
            option = input("Seleccione una opcion: ")
            # Show connected users
            if option == "1":
                client.get_contacts()
            # Add contact
            elif option == "2":
                user_to_add = input("Ingrese el nombre de usuario del usuario a agregar: ")
                subscription_message = input("Ingrese el mensaje de solicitud de subscripcion: ")
                client.add_contact(user_to_add, subscription_message)
                print("\nSubscripcion enviada")
            # Show contact details
            elif option == "3":
                user_to_search = input("Ingrese el nombre de usuario del usuario a buscar: ")
                client.search_user(user_to_search)
            # Send message to a user
            elif option == "4":
                print("\n1. enviar mensaje\n2. enviar archivo")
                message_option = input("Seleccione una opcion: ")
                # Send message
                if message_option == "1":
                    user_to_send = input("Ingrese el nombre de usuario del usuario a enviar el mensaje: ")
                    client.show_chat(user_to_send)
                    message = input("You: ")
                    client.send_message_to_user(user_to_send, message)
                # Send file
                elif message_option == "2":
                    user_to_send = input("Ingrese el nombre de usuario del usuario a enviar el archivo: ")
                    file_path = input("Ingrese el path del archivo a enviar: ")
                    client.send_file_to_user(user_to_send, file_path)
            # Create group
            elif option == "5":
                group_name = input("Ingrese el nombre del grupo: ")
                client.create_group(group_name)
                print("\nGrupo creado")
            # Join group
            elif option == "6":
                group_name = input("Ingrese el nombre del grupo: ")
                client.join_group(group_name)
                print("\nHas entrado al grupo")
            # Send message to group
            elif option == "7":
                group_to_send = input("Ingrese el nombre del grupo a enviar el mensaje: ")
                client.show_room_chat(group_to_send)
                message = input("You: ")
                client.send_message_to_group(group_to_send, message)
            # Send presence message
            elif option == "8":
                print("\n1. available\n2. away\n3. not available\n4. busy")
                value = input("Ingrese el valor de presencia: ")
                message = input("Ingrese el mensaje de presencia: ")
                show = get_show_precence(value)
                client.set_status(show, message)
            # Delete contact
            elif option == "9":
                user_to_delete = input("Ingrese el nombre de usuario del usuario a eliminar: ")
                client.delete_contact(user_to_delete)
                print("\nContacto eliminado")
            # Delete account
            elif option == "10":
                client.delete_account()
                print("\nCuenta eliminada")
                option = "11"
            # Logout
            elif option == "11":
                print("Cerrando sesion...")
                client.disconnect()
            # This is used to respond to a received message
            elif option == "Y" or option == "y":
                # If a new message is received waiting to be responded to
                if client.to_chat:
                    client.to_chat = False
                    # Message received from contact
                    if client.to_chat_type == "contact":
                        client.show_chat(client.message_receiver)
                        message = input("You: ")
                        client.send_message_to_user(client.message_receiver, message)
                    # Message received from group
                    else:
                        client.show_room_chat(client.message_receiver)
                        message = input("You: ")
                        client.send_message_to_group(client.message_receiver, message)
                else:
                    print("Operacion no valida")
            # Non valid options
            else:
                # This is used when user decides to not respond to a message
                if option == "n" or option == "N" and client.to_chat:
                    client.to_chat = False
                else:
                    print("Opcion no valida")
