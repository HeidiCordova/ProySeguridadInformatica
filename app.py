from flask import Flask, request, jsonify
from sistema_notas.sistema import SistemaNotas

app = Flask(__name__)
sistema = SistemaNotas()

# Ruta para verificar que el servidor está funcionando
@app.route('/')
def home():
    return jsonify({"message": "Sistema de notas universitarias API funcionando"})

# Ruta para autenticar usuario
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    clave = data.get('clave')
    
    usuario = sistema.autenticar_usuario(email, clave)
    if usuario:
        return jsonify({"message": f"¡Bienvenido, {usuario.nombre}!"})
    else:
        return jsonify({"error": "Autenticación fallida"}), 401

# Ruta para obtener todas las notas de un usuario
@app.route('/notas/<int:usuario_id>', methods=['GET'])
def obtener_notas(usuario_id):
    notas = sistema.obtener_notas_usuario(usuario_id)
    return jsonify([{"id": nota.id, "contenido": nota.contenido} for nota in notas])

# Ruta para crear una nueva nota
@app.route('/notas', methods=['POST'])
def crear_nota():
    data = request.json
    usuario_id = data.get('usuario_id')
    contenido = data.get('contenido')
    
    sistema.gestionar_notas(usuario_id, contenido)
    return jsonify({"message": "Nota creada exitosamente"})

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)

