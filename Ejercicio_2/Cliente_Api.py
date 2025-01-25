from collections import defaultdict

import requests

# URL base para la conexion con la API
BASE_URL = "http://127.0.0.1:5000"

# Objeto session para la persistencia del logeo del usuario
session = requests.Session()


# Funcion para iniciar la sesion con el usuario
def iniciar_sesion(session, base_url, nombre, passw):
    # Datos requeridos para el inicio de sesion del usuario
    cred = {
        "nombre": nombre,
        "pass": passw
    }

    # Indicamos el endpoint al que hacemos la peticion y le pasamos datos
    resp = session.post(f"{base_url}/login", json = cred)

    # En funcion de la respuesta obtenemos un return u otro
    if resp.status_code == 200:
        data = resp.json()
        print("Login exitoso:", data)
        return True
    else:
        print("Error en el inicio de sesion", resp.text())
        return False

# Funcion para cerrar la sesion del ususario que se encontraba conectado.
# Solo funciona con un login previo
def cerrar_sesion(session, base_url):
    # Accedemos al endpoint
    resp = session.post(f"{base_url}/logout")

    if resp.status_code == 200:
        print("Sesion cerrada")
        return True
    else:
        print("Error en el cierre de sesion")
        return False

# Funcion para escribir mensajes a otros usuarios
# Solo funciona con un login previo
def enviar_mensaje(session, base_url, texto, id_receptor):
    # Datos requeridos para realizar el envio del mensaje
    cred = {
        "contenido": texto,
        "id_receptor": id_receptor
    }

    # Acceso al endpoint requerido enviando los datos almacenados anteriormente
    resp = session.post(f"{base_url}/message", json = cred)

    if resp.status_code == 201:
        data = resp.json()
        print("Mensaje enviado:", data)
        return True
    else:
        print("Error en el envio del mensaje", resp.text)
        return False

# Funcion para leer los mensajes del usuario, tanto enviados como resibidos
# Solo funciona con un login previo
def leer_mensajes(session, base_url):
    # Acceso al endpoint
    resp = session.get(f"{base_url}/message")

    if resp.status_code == 200:
        data = resp.json()
        print("Aqui se muestran los mensajes en los que apareces:", data)
    else:
        print("No se han podido recuperar los mensajes", resp.text)

if __name__ == '__main__':
    # Bucle que mostrara un menu con diferentes opciones al usuario
    menu = True
    while menu:
        print("Selecciona una opcion:")
        print("1.- Iniciar sesion")
        print("2.- Cerrar sesion")
        print("3.- Enviar un mensaje")
        print("4.- Leer mis mensajes")
        print("Otro.- Salir")
        opc = input()

        match opc:
            case "1":
                nom = input("Introduce el nombre de usuario")
                passw = input("Inserte la contraseña")
                iniciar_sesion(session, BASE_URL, nom, passw)
            case "2":
                cerrar_sesion(session, BASE_URL)
            case "3":
                id_r = print("Indica el numero de id del usuario al que mandar el mensaje")
                cont = input("Escribe un mensaje")
                enviar_mensaje(session, BASE_URL, cont, id_r)
            case "4":
                leer_mensajes(session, BASE_URL)
            case defaultdict:
                print("Cerrando conexion")
                menu = False



