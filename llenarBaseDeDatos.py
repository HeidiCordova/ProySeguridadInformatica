from sistema_notas.sistema import SistemaNotas
# Crear instancia del sistema
sistema = SistemaNotas()

# Función para inicializar datos en la base de datos
def inicializar_datos():
    # Crear roles iniciales
    roles = [
        ("admin", "crear_usuario,gestionar_notas"),
        ("profesor", "ver_notas,editar_notas"),
        ("estudiante", "ver_notas,crear_notas")
    ]
    # Registrar roles
    registrar_roles(roles)

    # Crear usuarios iniciales
    usuarios = [
        (1, "Alice", "alice@example.com", "password123", "admin"),
        (2, "Bob", "bob@example.com", "securepass", "profesor"),
        (3, "Charlie", "charlie@example.com", "mypass", "estudiante"),
    ]
    registrar_usuarios(usuarios)

    # Crear notas iniciales
    notas = [
        ("Nota de Alice", 1),
        ("Nota de Bob", 2),
        ("Nota de Charlie", 3),
    ]
    registrar_notas(notas)

    print("Base de datos creada con datos iniciales.")

# Función para registrar roles
def registrar_roles(roles):
    for nombre, permisos in roles:
        # Verifica si el rol ya existe
        conexion = sistema.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT COUNT(*) FROM roles WHERE nombre = ?', (nombre,))
        if cursor.fetchone()[0] == 0:
            # Si no existe, agrégalo
            sistema.agregar_rol(nombre, permisos.split(','))
        conexion.close()

# Función para registrar usuarios
def registrar_usuarios(usuarios):
    for id, nombre, email, clave, rol in usuarios:
        sistema.registrar_usuario(id, nombre, email, clave, rol)

# Función para registrar notas
def registrar_notas(notas):
    for contenido, usuario_id in notas:
        sistema.gestionar_notas(usuario_id, contenido)

# Ejecutar la inicialización
if __name__ == "__main__":
    inicializar_datos()

