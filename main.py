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
9. Salir
'''

option = ""

while option != "9":
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
        user_to_send = input("Ingrese el nombre de usuario del usuario a enviar el mensaje: ")
        message = input("Ingrese el mensaje a enviar: ")
        client.send_message_to_user(user_to_send, message)
    elif option == "5":
        group_name = input("Ingrese el nombre del grupo: ")
        client.create_group(group_name)
        print("\nGrupo creado")
    elif option == "6":
        group_name = input("Ingrese el nombre del grupo: ")
        client.join_group(group_name)
        print("\nUsuario agregado")
    elif option == "7":
        group_to_send = input("Ingrese el nombre del grupo a enviar el mensaje: ")
        message = input("Ingrese el mensaje a enviar: ")
        client.send_message_to_group(group_to_send, message)
    elif option == "8":
        pass
    elif option == "9":
        print("Saliendo...")
        client.disconnect()
        exit()
    else:
        print("Opcion no valida")
