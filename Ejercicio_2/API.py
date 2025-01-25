
import mysql.connector
from flask import Flask, request, jsonify, session
from mysql.connector import Error

app = Flask(__name__)

# Clave para controlar los logins
app.secret_key = "mi_super_clave_secreta"

# Creamos la conexion con la base de datos (MySQL Workbench)
def crear_conexion():
    conn = None
    try:
        # Hacemos la conexion pasando el usuario, contraseña, host y la bbdd a la que conectarnos
        conn = mysql.connector.connect(user='root', password='toor', host='127.0.0.1', database='comunicacion_usuarios')
        if conn.is_connected():
            print("Conectado a la BBDD")
    except Error as e:
        print(f"Error: {e}")

    return conn

# Almacenamos la conexion
conn = crear_conexion()
# Objeto necesario para realizar las consultas SQL
cursor = conn.cursor(dictionary=True)

# Ruta que devuelve todos los usuarios registrados en la bbdd.
# Su funcionamiento no esta implementada en el cliente
@app.route('/users', methods=['GET'])
def mostrar_ususarios():
    try:
        # Consulta a realizar
        cursor.execute("SELECT * FROM users")
        # Almacenamos los resultados obtenidos y los devolvermos en formato json
        usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except Error as e:
        return jsonify({"Error": str(e)})

# Ruta que permite registrar nuevos usuarios. Se controla que el nombre se usuario no este en uso.
# Si el nombre es repetido informa al usuario y no realiza el registro.
@app.route('/users', methods=['POST'])
def registrar_ususario():
    try:
        # Obtenemos la informacion del json necesario para el POST
        user = request.json
        # Procedemos a controlar que el nombre del usuario no este registrado
        # Ejecutamos la consulta introduciendo los datos necesarios obtenidos del json
        cursor.execute("SELECT nombre, pass FROM users WHERE nombre = %s",(user["nombre"],))
        existe = cursor.fetchone()
        # Si el nombre ya existe en la bbddd informa al usuario, en caso contrario coge el resto de informacion
        # del json y la usa para generar una consulta de insert
        if existe:
            return jsonify({"Error": "nombre de ususario registrado"})
        else:
            cursor.execute("INSERT INTO users (nombre, edad, pass) VALUES (%s, %s, %s)",
                           (user["nombre"], user["edad"], user["pass"]))
            conn.commit()
            # Devuelve el id que se le ha asignado al nuevo usuario
            return jsonify({"id": cursor.lastrowid})
    except Error as e:
        return jsonify({"Error": str(e)})

# Funcion que permite iniciar sesion a usuarios ya registrados. No es seguro ya que almacena la contraseña en texto plano
@app.route('/login', methods=['POST'])
def iniciar_sesion():
    # Obtenemos la informacion del json necesario y la almacenamos en variables
    data = request.json
    nombre = data.get("nombre")
    passw = data.get("pass")

    # Compruebo que el ususario y la contraseña coincidan
    cursor.execute("SELECT id FROM users WHERE nombre = %s AND pass = %s", (nombre, passw))
    user = cursor.fetchone()
    # Si los datos estan correctos creo una sesion que mantengo hasta hacer un logout
    if user:
        session['user_id'] = user['id']
        return jsonify({"mensaje": "Inicio de sesión correcto"}), 200
    else:
        return jsonify({"Error": "Ususario o contraseña incorrectos"})

# Funcion para cerrar la sesion de un usuario iniciado previamente
@app.route('/logout', methods=['POST'])
def cerrar_sesion():
    # Con este metodo eliminamos el valor almacenado en user_id en la sesion Flask, para que no haya un usuario conectado
    session.pop('user_id', None)
    return jsonify({"mensaje": "Sesion cerrada"}), 200

# Funcion que permite enviar mensajes a otros usuarios.
@app.route('/message', methods=['POST'])
def enviar_mensaje():
    # Controlamos que haya un usuario iniciado para poder mandar un mensaje
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"Error": "Debes iniciar sesion para mandar mensajes"}), 401

    # Tratamos los datos recibidos del fichero json
    data = request.json
    id_receptor = data.get("id_receptor")
    contenido = data.get("contenido")

    # Verificamos que se hayan adjuntado los datos necesarios
    if not id_receptor or not contenido:
        return jsonify({"Error": "Faltan datos"})

    # Aseguramos que el receptor exista en nuestra bbdd
    cursor.execute("SELECT id FROM users WHERE id = %s", (data["id_receptor"],))
    existe = cursor.fetchone()

    if not existe:
        return jsonify({"Error": "El usuario indicado no existe"})

    try:
        # Ejecutamos la consulta para insertar el mensaje en la tabla con los datos correspondientes
        cursor.execute(
            "INSERT INTO messages (contenido, id_emisor, id_receptor) VALUES (%s, %s, %s)",
            (contenido, user_id, id_receptor)
        )
        conn.commit()
        return jsonify({
            "Mensaje": "Mensaje enviado con exito",
            "message_id": cursor.lastrowid
        }), 201
    except Error as e:
        return jsonify({"Error": str(e)}), 500

# Funcion que permite a un usuario leer todos los mensajes que ha mandado o recibido
@app.route('/message', methods=['GET'])
def leer_mensaje():
    # Verificamos que haya una sesion de un usuario iniciada
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"Error": "Debes iniciar sesion para leer mensajes"}), 401

    try:
        # Obtenemos y mostramos todos los menajes
        cursor.execute(
            "SELECT * FROM messages WHERE id_emisor = %s OR id_receptor = %s",
            (user_id, user_id)
        )
        mensajes = cursor.fetchall()
        return jsonify(mensajes)

    except Error as e:
        return jsonify({"Error": str(e)}), 500


# Iniciamos el servidor
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

