import sqlite3
import bcrypt
from sistema_notas.usuario import Usuario
from sistema_notas.rol import Rol
from sistema_notas.nota import Nota

class SistemaNotas:
    def __init__(self, db_path="sistema_notas.db"):
        self.db_path = db_path
        self._crear_tablas()

    def _crear_tablas(self):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()

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

        conexion.commit()
        conexion.close()

    def registrar_usuario(self, id, nombre, email, clave, rol):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO usuarios (id, nombre, email, clave, rol) VALUES (?, ?, ?, ?, ?)',
                       (id, nombre, email, clave, rol))
        conexion.commit()
        conexion.close()

    def autenticar_usuario(self, email, clave):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute('SELECT id, nombre, email, clave, rol FROM usuarios WHERE email = ?', (email,))
        usuario_data = cursor.fetchone()
        conexion.close()

        if usuario_data and bcrypt.checkpw(clave.encode('utf-8'), usuario_data[3].encode('utf-8')):
            return Usuario(*usuario_data)
        return None

    def agregar_rol(self, nombre, permisos):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO roles (nombre, permisos) VALUES (?, ?)', (nombre, ",".join(permisos)))
        conexion.commit()
        conexion.close()

    def gestionar_notas(self, usuario_id, contenido):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO notas (contenido, usuario_id) VALUES (?, ?)', (contenido, usuario_id))
        conexion.commit()
        conexion.close()
    def verificar_tablas(self):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        conexion.close()
    
    def listar_tablas(self):
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        conexion.close()
        return tablas
