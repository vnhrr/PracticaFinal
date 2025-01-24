import base64
from crypt import methods

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from flask import Flask, jsonify, request

from Ejercicio_1.Servidor import descifrar

app = Flask(__name__)

usuarios = [
    {"id": 0, "nombre": "admin", "pass": "admin", "mensajes": []},
    {"id": 1, "nombre": "Ivan", "pass": "1234"}
]


@app.route('/')
def home():
    return "Estas haciendo una API"


@app.route('/api/usuarios', methods=['GET'])
def mostrar_usuarios():
    usuarios_muestra = []
    global usuarios
    for u in usuarios:
        if u["nombre"] != "admin":
            muestra_usu = {
                "id": u["id"],
                "nombre": u["nombre"]
            }
            usuarios_muestra.append(muestra_usu)

    return jsonify(usuarios_muestra)


@app.route('/api/register', methods=['POST'])
def registrar():
    data = request.get_json()
    if not data:
        return jsonify({"Error": "No se proporcioanor datos"}), 400

    usuario = data.get("nombre", "Nombre ususario")
    nombe_usu = next((u for u in usuarios if u["nombre"] == usuario), None)
    if usuario != nombe_usu:
        id = usuarios[-1]["id"] + 1
        nuevo_usu = {
            "id": id,
            "nombre": usuario
        }
        usuarios.append(nuevo_usu)
        return jsonify(nuevo_usu)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"Error": "No se han proporcionado datos"})

    acceso = False
    for u in usuarios:
        if (u["nombre"] == data.get("nombre")) and (u["pass"] == data.get("pass")):
            acceso = True
            return "Has accedido" and True

    if not acceso:
        return "Nombre o password incorrectos"


@app.route("/api/send", methods=['POST'])
def enviar():
    def cifrar(texto):
        clave = get_random_bytes(16)
        iv = get_random_bytes(16)
        cipher = AES.new(clave, AES.MODE_CBC, iv)
        bloque = 16

        padding = bloque - (len(texto.encode('UTF-8')) % bloque)
        texto_padded = texto.encode('UTF-8') + bytes([padding]) * padding

        return cipher.encrypt(texto_padded)

    data = request.get_json()
    if not data:
        return jsonify({"Error": "No se han proporcionado datos"})

    usu = data.get("nombre")
    mens = data.get("mensaje")
    mens_cod = cifrar(mens)

    enviado = False
    for u in usuarios:
        if u["nombre"] == usu:
            u["mensajes"].append(mens_cod)
            enviado = True

    if enviado:
        return jsonify("Mensaje enviado")


@app.route("/api/messages", methods=['GET'])
def leer():
    def leer_clave_iv(nombre_archivo):
        # Leer clave e IV del archivo
        with open(nombre_archivo, "r") as archivo:
            lineas = archivo.readlines()
            clave = base64.b64decode(lineas[0].strip())  # Decodificar Base64
            iv = base64.b64decode(lineas[1].strip())  # Decodificar Base64

        return clave, iv

    def descifrar(datos):
        clave, iv = leer_clave_iv("clave_iv_API.txt")
        decipher = AES.new(clave, AES.MODE_CBC, iv)
        texto_des_pad = decipher.decrypt(datos)

        ultimo_bloque = texto_des_pad[-1]
        texto_des = texto_des_pad[:ultimo_bloque]

        return texto_des.decode('UTF-8')

    data = request.get_json()
    if not data:
        return jsonify({"Error": "No se han proporcionado datos"})

    if login():
        for u in usuarios:
            if u["nombre"] == data.get("nombre"):
                for mens in u["mensajes"]:
                    correo = descifrar(mens)
                    return jsonify(correo)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
