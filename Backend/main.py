from flask import Flask, request, jsonify
import redis
import sqlite3
import pyotp
from flask_cors import CORS
import qrcode
import base64
from io import BytesIO
from sistema_notas.sistema import SistemaNotas


# Configuración de la aplicación Flask
app = Flask(__name__)
CORS(app) 
sistema = SistemaNotas()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Configuración de seguridad
BLOQUEO_TIEMPO = 300  # 5 minutos
MAX_INTENTOS = 3




# ================== RUTAS FLASK ==================

@app.errorhandler(Exception)
def manejar_excepciones(e):
    """Manejador global de errores"""
    return manejar_error(f"Error del servidor: {str(e)}", 500)


# RUTA PARA VERIFICAR MFA
@app.route('/api/verificarCodigoMFA', methods=['POST'])
def verificar_mfa_ruta():
    data = request.json
    usuario_id = data.get('usuario_id')
    codigo_mfa = data.get('codigo_mfa')

    if not usuario_id or not codigo_mfa:
        return manejar_error("ID de usuario y código MFA son requeridos", 400)

    usuario = sistema.obtener_usuario_por_id(usuario_id)
    if not usuario or not usuario.mfa_secret:
        return manejar_error("Usuario no encontrado o MFA no habilitado", 404)

    error = verificar_codigo_mfa(usuario, codigo_mfa)
    if error:
        return error

    reset_intentos(usuario.email)
    return jsonify({"message": "Inicio de sesión exitoso"}), 200


# RUTA PARA HABILITAR MFA
import qrcode
import base64
from io import BytesIO

@app.route('/api/habilitarMFA', methods=['POST'])
def habilitar_mfa():
    data = request.json
    usuario_id = data.get('usuario_id')

    if not usuario_id:
        return manejar_error("ID de usuario requerido", 400)

    usuario = sistema.obtener_usuario_por_id(usuario_id)
    if not usuario:
        return manejar_error("Usuario no encontrado", 404)

    resultado = sistema.habilitar_mfa(usuario_id)

    # resultado["qr_url"] contiene el provisioning URI (otpauth://totp/...)

    # Generar el código QR en el backend
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(resultado["qr_url"])
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convertir la imagen a Base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Ahora devolvemos el QR como Base64
    return jsonify({
        "message": "MFA habilitado con éxito",
        "qr_url": resultado["qr_url"],
        "qr_image_base64": img_str
    }), 200



# RUTA PARA AGREGAR USUARIO
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    clave = data.get('clave')
    rol = data.get('rol')

    if not all([nombre, email, clave, rol]):
        return manejar_error("Todos los campos son requeridos", 400)

    try:
        sistema.registrar_usuario(None, nombre, email, clave, rol)
        usuario = sistema.autenticar_usuario(email, clave)
        return jsonify({"id": usuario.id, "message": "Usuario registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return manejar_error("El correo ya está registrado", 400)
    except Exception as e:
        return manejar_error(f"Error del servidor: {str(e)}", 500)


# RUTA PARA INICIAR SESIÓN
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    clave = data.get('clave')

    if not email or not clave:
        return manejar_error("Correo y clave son requeridos", 400)

    if esta_bloqueado(email):
        return manejar_error("Usuario bloqueado temporalmente. Inténtalo más tarde.", 403)

    usuario = autenticar_usuario(email, clave)
    if isinstance(usuario, tuple):
        # Esto indica que la función autenticar_usuario devolvió un error (manejar_error)
        return usuario

    # Si llegamos aquí, las credenciales son correctas
    if usuario.mfa_secret:
        # El usuario ya tiene MFA habilitado, lo requerimos
        return jsonify({
            "message": "Se requiere autenticación multifactor",
            "mfa_required": True,
            "usuario_id": usuario.id,
            "rol": usuario.rol
        }), 200
    else:
        # Usuario sin MFA habilitado
        # Aquí podemos decidir si queremos siempre ofrecer MFA o basarlo en alguna condición.
        # Por ahora, asumiendo que el usuario siempre puede habilitar MFA si no lo tiene.
        reset_intentos(email)
        return jsonify({
            "message": "Inicio de sesión exitoso, ¿deseas habilitar MFA?",
            "mfa_required": False,
            "mfa_can_enable": True,  # <-- agregamos este campo
            "usuario_id": usuario.id, # Será útil en el front para habilitar MFA
            "rol": usuario.rol
        }), 200




# LISTAR NOTAS
@app.route('/api/notas', methods=['GET'])
def listar_notas():
    """Lista las notas de un usuario dado su ID."""
    usuario_id = request.args.get('usuario_id')
    if not usuario_id:
        return manejar_error("Falta el ID del usuario", 400)
    if not sistema.existe_usuario(usuario_id):
        return manejar_error("El usuario no existe", 404)
    notas = sistema.obtener_notas_usuario(usuario_id)
    if not notas: 
        return jsonify({"message": "Este usuario no tiene notas cargadas"}), 200
    return jsonify(notas), 200


# LISTAR USUARIOS
@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = sistema.listar_usuarios()
    return jsonify(usuarios)



# ================== FUNCIONES AUXILIARES ==================

def esta_bloqueado(email):
    return redis_client.get(f"bloqueo:{email}") is not None


def registrar_intento_fallido(email):
    intentos = redis_client.incr(f"intentos:{email}")
    if intentos == 1:
        redis_client.expire(f"intentos:{email}", BLOQUEO_TIEMPO)
    if intentos >= MAX_INTENTOS:
        redis_client.setex(f"bloqueo:{email}", BLOQUEO_TIEMPO, "bloqueado")
        redis_client.delete(f"intentos:{email}")
        return True
    return False


def reset_intentos(email):
    redis_client.delete(f"intentos:{email}")
    redis_client.delete(f"bloqueo:{email}")


def manejar_error(mensaje, codigo):
    """Formato uniforme de errores"""
    return jsonify({"error": mensaje}), codigo


def autenticar_usuario(email, clave):
    """Autentica al usuario y maneja intentos fallidos"""
    if not email or not clave:
        return manejar_error("Credenciales incompletas", 400)
    
    usuario = sistema.autenticar_usuario(email, clave)
    if not usuario:
        if registrar_intento_fallido(email):
            return manejar_error("Demasiados intentos fallidos. Usuario bloqueado temporalmente.", 403)
        return manejar_error("Autenticación fallida", 401)
    print(usuario)
    return usuario


def verificar_codigo_mfa(usuario, codigo_mfa):
    """Verifica el código MFA si está habilitado"""
    if usuario.mfa_secret:
        if not codigo_mfa:
            return manejar_error("Se requiere el código MFA", 403)
        totp = pyotp.TOTP(usuario.descifrar_mfa_secret())
        if not totp.verify(codigo_mfa):
            registrar_intento_fallido(usuario.email)
            return manejar_error("Código MFA incorrecto", 401)
    return None



# INICIAR APLICACIÓN
if __name__ == '__main__':
    app.run(debug=True)

