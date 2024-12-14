from flask import Flask, request, jsonify
import bcrypt
import sqlite3
import redis

# Función para verificar permisos
def verificar_permiso(rol, permiso):
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    cursor.execute("SELECT permisos FROM roles WHERE nombre = ?", (rol,))
    permisos = cursor.fetchone()
    conexion.close()
    return permisos and permiso in permisos[0].split(',')

app = Flask(__name__)

db_path = "sistema_notas.db"
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Ruta para agregar un usuario
@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    if not verificar_permiso(request.json['rol'], 'crear_usuario'):
        return jsonify({"error": "Acción no permitida"}), 403
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    clave = bcrypt.hashpw(data.get('clave').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    rol = data.get('rol', 'usuario')  # Valor predeterminado para el rol

    try:
        conexion = sqlite3.connect(db_path)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, clave, rol) VALUES (?, ?, ?, ?)", (nombre, email, clave, rol))
        conexion.commit()
        conexion.close()
        return jsonify({"message": "Usuario agregado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El correo electrónico ya está registrado"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para listar usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        conexion = sqlite3.connect(db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, email, rol FROM usuarios")
        usuarios = cursor.fetchall()
        conexion.close()

        # Convertir usuarios a un formato JSON-friendly
        usuarios_json = [{"id": u[0], "nombre": u[1], "email": u[2], "rol": u[3]} for u in usuarios]
        return jsonify(usuarios_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Configuración de seguridad
BLOQUEO_TIEMPO = 300  # Tiempo de bloqueo en segundos (5 minutos)
MAX_INTENTOS = 3  # Número máximo de intentos fallidos permitidos

# Verifica si un usuario está bloqueado
def esta_bloqueado(email):
    bloqueado = redis_client.get(f"bloqueo:{email}")
    return bloqueado is not None

# Incrementa intentos fallidos y maneja bloqueo
def registrar_intento_fallido(email):
    intentos = redis_client.incr(f"intentos:{email}")
    if intentos == 1:
        redis_client.expire(f"intentos:{email}", BLOQUEO_TIEMPO)
    if intentos >= MAX_INTENTOS:
        redis_client.setex(f"bloqueo:{email}", BLOQUEO_TIEMPO, "bloqueado")
        redis_client.delete(f"intentos:{email}")
        return True
    return False

# Resetea intentos fallidos tras un inicio de sesión exitoso
def reset_intentos(email):
    redis_client.delete(f"intentos:{email}")
    redis_client.delete(f"bloqueo:{email}")

# Ruta para autenticar usuario (sin MFA)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    clave = data.get('clave')

    # Verificar si el usuario está bloqueado
    if esta_bloqueado(email):
        return jsonify({"error": "Usuario bloqueado temporalmente. Inténtalo más tarde."}), 403

    # Conectar a la base de datos y verificar credenciales
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    cursor.execute('SELECT id, nombre, email, clave FROM usuarios WHERE email = ?', (email,))
    usuario_data = cursor.fetchone()
    conexion.close()

    if usuario_data and bcrypt.checkpw(clave.encode('utf-8'), usuario_data[3].encode('utf-8')):
        # Reiniciar contador de intentos fallidos
        reset_intentos(email)
        return jsonify({"message": "Inicio de sesión exitoso"})
    else:
        # Registrar intento fallido
        if registrar_intento_fallido(email):
            return jsonify({"error": "Demasiados intentos fallidos. Usuario bloqueado temporalmente."}), 403

        return jsonify({"error": "Autenticacion fallida"}), 401
    
@app.route('/notas', methods=['GET'])
def listar_notas():
    usuario_id = request.args.get('usuario_id')
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    cursor.execute("SELECT contenido FROM notas WHERE usuario_id = ?", (usuario_id,))
    notas = cursor.fetchall()
    conexion.close()
    return jsonify([{"contenido": nota[0]} for nota in notas])

if __name__ == '__main__':
    app.run(debug=True)
