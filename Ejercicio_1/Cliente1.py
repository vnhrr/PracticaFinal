import socket
from Crypto.Cipher import AES  # Para manejar el cifrado y descifrado con AES
import base64  # Para convertir los datos cifrados a Base64 y facilitar su lectura o transmisión

# Leo y retorno la clave y el iv que he generado anterior mente con otro programa,
# la cual me servira para codificar el mensaje que voy a mandar al servidor.
def leer_clave_iv(nombre_archivo):
    with open(nombre_archivo, "r") as archivo:
        lineas = archivo.readlines()
        # Decodifico y almaceno en una variable
        clave = base64.b64decode(lineas[0].strip())
        iv = base64.b64decode(lineas[1].strip())

    # Retorno la clave y el iv
    return clave, iv

# Funcion para cifrar el texto, devuelve el mensaje cifrado
def cifrar_aes(texto, clave, iv):
    cipher = AES.new(clave, AES.MODE_CBC, iv)
    bloque = 16

    padding = bloque - (len(texto.encode('UTF-8')) % bloque)
    texto_padded = texto.encode('UTF-8') + (bytes([padding]) * padding)

    return cipher.encrypt(texto_padded)

# Mando el mensaje al servidor
def enviar_mens():
    # Creo socket y conecto con el servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 5010))
    # Obtengo la clave y el iv del fichero en el que se han almacenado
    clave, iv = leer_clave_iv("clave_iv.txt")
    mens = "Hola servidor"
    # Cifro el mensaje
    mens_cifr = cifrar_aes(mens, clave, iv)
    # Codifico el mensaje cifrado en base64 para mandarlo al servidor
    mensaje_cifrado_b64 = base64.b64encode(mens_cifr).decode('utf-8')
    print("Mensaje original:", mens)
    print("Mensaje cifrado (Base64):", mensaje_cifrado_b64)

    # Envio el mensaje
    s.send(mensaje_cifrado_b64.encode())

if __name__ == '__main__':
    enviar_mens()


