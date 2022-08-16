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

option = ""
client = None

while option != "3" and not is_authenticated:
    print(menu_login)
    option = input("Seleccione una opcion: ")
    if option == "1":
        username = input("\nIngrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")
        if username == 'jurhs':
            password = "91vGs55@hHjJ"
        client = Client(username + SERVER, password)
        print("\nIniciando sesion...")
        if client.login():
            is_authenticated = True
            print("\nSesion iniciada")
        else:
            print("\nError al iniciar sesion")
    elif option == "2":
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
    elif option == "3":
        print("Saliendo...")
    else:
        print("Opcion no valida")

if not is_authenticated:
    exit()

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

option = ""

while option != "11":
    print(menu)
    option = input("Seleccione una opcion: ")
    if option == "1":
        client.get_contacts()
    elif option == "2":
        user_to_add = input("Ingrese el nombre de usuario del usuario a agregar: ")
        subscription_message = input("Ingrese el mensaje de solicitud de subscripcion: ")
        client.add_contact(user_to_add, subscription_message)
        print("\nSubscripcion enviada")
    elif option == "3":
        user_to_search = input("Ingrese el nombre de usuario del usuario a buscar: ")
        client.search_user(user_to_search)
    elif option == "4":
        print("\n1. enviar mensaje\n2. enviar archivo")
        message_option = input("Seleccione una opcion: ")
        if message_option == "1":
            user_to_send = input("Ingrese el nombre de usuario del usuario a enviar el mensaje: ")
            client.show_chat(user_to_send)
            message = input("You: ")
            client.send_message_to_user(user_to_send, message)
        elif message_option == "2":
            user_to_send = input("Ingrese el nombre de usuario del usuario a enviar el archivo: ")
            file_path = input("Ingrese el path del archivo a enviar: ")
            client.send_file_to_user(user_to_send, file_path)
    elif option == "5":
        group_name = input("Ingrese el nombre del grupo: ")
        client.create_group(group_name)
        print("\nGrupo creado")
    elif option == "6":
        group_name = input("Ingrese el nombre del grupo: ")
        client.join_group(group_name)
        print("\nHas entrado al grupo")
    elif option == "7":
        group_to_send = input("Ingrese el nombre del grupo a enviar el mensaje: ")
        client.show_room_chat(group_to_send)
        message = input("You: ")
        client.send_message_to_group(group_to_send, message)
    elif option == "8":
        print("\n1. available\n2. away\n3. not available\n4. busy")
        value = input("Ingrese el valor de presencia: ")
        message = input("Ingrese el mensaje de presencia: ")
        show = ""
        if value == "1":
            show = "available"
        elif value == "2":
            show = "away"
        elif value == "3":
            show = "xa"
        elif value == "4":
            show = "dnd"
        client.set_status(show, message)
    elif option == "9":
        user_to_delete = input("Ingrese el nombre de usuario del usuario a eliminar: ")
        client.delete_contact(user_to_delete)
        print("\nContacto eliminado")
    elif option == "10":
        client.delete_account()
        print("\nCuenta eliminada")
        option = "11"
        exit()
    elif option == "11":
        print("Saliendo...")
        client.disconnect()
        exit()
    elif option == "Y" or option == "y":
        if client.to_chat:
            client.to_chat = False
            if client.to_chat_type == "contact":
                client.show_chat(client.message_receiver)
                message = input("You: ")
                client.send_message_to_user(client.message_receiver, message)
            else:
                client.show_room_chat(client.message_receiver)
                message = input("You: ")
                client.send_message_to_group(client.message_receiver, message)
    else:
        if option == "n" or option == "N" and client.to_chat:
            client.to_chat = False
        else:
            print("Opcion no valida")
