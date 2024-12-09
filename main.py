import sqlite3
import bcrypt

# Crear conexión a la base de datos
db_path = "sistema_notas.db"
conexion = sqlite3.connect(db_path)
cursor = conexion.cursor()

# Crear tablas
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    clave TEXT NOT NULL,
    rol TEXT NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    permisos TEXT NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contenido TEXT NOT NULL,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
)''')

# Roles iniciales
roles = [
    ("admin", "crear_usuario,gestionar_notas"),
    ("profesor", "ver_notas,editar_notas"),
    ("estudiante", "ver_notas,crear_notas")
]

# Crear roles iniciales sin duplicados
for rol in roles:
    cursor.execute('SELECT COUNT(*) FROM roles WHERE nombre = ?', (rol[0],))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO roles (nombre, permisos) VALUES (?, ?)', rol)

# Crear usuarios iniciales
usuarios = [
    (1, "Alice", "alice@example.com", bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode('utf-8'), "admin"),
    (2, "Bob", "bob@example.com", bcrypt.hashpw(b"securepass", bcrypt.gensalt()).decode('utf-8'), "profesor"),
    (3, "Charlie", "charlie@example.com", bcrypt.hashpw(b"mypass", bcrypt.gensalt()).decode('utf-8'), "estudiante"),
]

# Insertar usuarios sin duplicados
for usuario in usuarios:
    cursor.execute('SELECT COUNT(*) FROM usuarios WHERE email = ?', (usuario[2],))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO usuarios (id, nombre, email, clave, rol) VALUES (?, ?, ?, ?, ?)', usuario)

# Crear notas iniciales
notas = [
    ("Nota de Alice", 1),
    ("Nota de Bob", 2),
    ("Nota de Charlie", 3),
]

# Insertar notas sin duplicados
for nota in notas:
    cursor.execute('SELECT COUNT(*) FROM notas WHERE contenido = ? AND usuario_id = ?', nota)
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO notas (contenido, usuario_id) VALUES (?, ?)', nota)

# Confirmar cambios y cerrar conexión
conexion.commit()
conexion.close()

print("Base de datos creada con datos iniciales.")
