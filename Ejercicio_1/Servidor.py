import base64
import socket
import threading
import time
from datetime import datetime
from platform import system
from sqlite3 import Time
from threading import Timer

from Crypto.Cipher import AES

# Metodo para descifrar el mensaje que me llegue del cliente
def descifrar(datos, clave, iv):
    decipher = AES.new(clave, AES.MODE_CBC, iv)
    texto_des_pad = decipher.decrypt(datos)

    ultimo_bloque = texto_des_pad[-1]
    texto_des = texto_des_pad[:ultimo_bloque]

    return texto_des.decode('UTF-8')

# Controlo varios clientes
def servidor_hilos():
    # Creo socket, intalo el servidor en la ip y puerto de preferencia y pongo a escuchar un maximo de 2 conexiones
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 5010))
    s.listen(2)
    # Bucle que mantendra al servidor escuchando indefinidamente
    while True:
        conn, addr = s.accept()
        hilo = threading.Thread(target=manejar_hilo, args=(conn, addr))
        # Imprimo la direccion, puerto y la hora de conexion
        print(f"{addr}, {time.ctime()}")
        hilo.start()

# Metodo para controlar lo que quiero hacer con cada cliente que se conecte
def manejar_hilo(conn, addr):
    activo = True
    while activo:
        datos = conn.recv(1024)
        if not datos:
            activo = False

        # Obtengo la clave y el iv para decodifica del fichero correspondiente
        clave, iv = leer_clave_iv("clave_iv.txt")
        # Obtenfo el mensaje que me ha mandado el cliente y obtengo el mensaje en base64
        datos_cifr_b64 = datos.decode()
        # Decodifico la base64 para obtener el mensaje en crudo para aplicar el descifrado
        datos_cifr = base64.b64decode(datos_cifr_b64)
        # Guardo en una variable el mensaje descifrado
        mens = descifrar(datos_cifr, clave, iv)
        # Imprimo el mensaje
        print(mens)

# Leo y retorno la clave y el iv que he generado anterior mente con otro programa,
# la cual me servira para codificar el mensaje que voy a mandar al servidor.
def leer_clave_iv(nombre_archivo):
    with open(nombre_archivo, "r") as archivo:
        lineas = archivo.readlines()
        # Decodifico y almaceno en una variable
        clave = base64.b64decode(lineas[0].strip())
        iv = base64.b64decode(lineas[1].strip())

    return clave, iv

if __name__ == '__main__':
    servidor_hilos()


