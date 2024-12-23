import sqlite3 
import bcrypt
import pyotp

from sistema_notas.usuario import Usuario
#from usuario import Usuario


class SistemaNotas:
    def __init__(self, db_path="sistema_notas.db"):
        self.db_path = db_path
        self._crear_tablas()

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    # Método para crear la base de datos
    def _crear_tablas(self):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL,
            rol TEXT NOT NULL,
            mfa_secret TEXT
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




    # Manejo de usuarios
    def registrar_usuario(self, id, nombre, email, clave, rol):
        usuario = Usuario(id, nombre, email, clave, rol)
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO usuarios (id, nombre, email, clave, rol) VALUES (?, ?, ?, ?, ?)',
                       (usuario.id, usuario.nombre, usuario.email, usuario.clave.decode('utf-8'), usuario.rol))
        conexion.commit()
        conexion.close()

    def autenticar_usuario(self, email, clave):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT id, nombre, email, clave, rol, mfa_secret FROM usuarios WHERE email = ?', (email,))
        usuario_data = cursor.fetchone()
        conexion.close()

        if usuario_data and bcrypt.checkpw(clave.encode('utf-8'), usuario_data[3].encode('utf-8')):
            return Usuario(*usuario_data)
        return None
    
    def listar_usuarios(self):
        try:
            conexion = self.get_db_connection()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, email, rol FROM usuarios")
            usuarios = cursor.fetchall()
            conexion.close()
            # Devolver datos correctamente estructurados
            return [{"id": u[0], "nombre": u[1], "email": u[2], "rol": u[3]} for u in usuarios]
        
        except sqlite3.Error as e:
            # Manejo de errores específicos de SQLite
            return {"error": f"Error de base de datos: {str(e)}"}
        
        except Exception as e:
            # Manejo de cualquier otro error inesperado
            return {"error": f"Error inesperado: {str(e)}"}
    
    def obtener_usuario_por_id(self, usuario_id):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()

        # Consulta al usuario por ID
        cursor.execute(
            'SELECT id, nombre, email, clave, rol, mfa_secret FROM usuarios WHERE id = ?',
            (usuario_id,)
        )
        usuario_data = cursor.fetchone()
        conexion.close()

        # Verifica si existe el usuario
        if usuario_data:
            id, nombre, email, clave, rol, mfa_secret = usuario_data
            return Usuario(id, nombre, email, clave, rol, mfa_secret)
        
        return None
    
    def existe_usuario(self, usuario_id):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT 1 FROM usuarios WHERE id = ?', (usuario_id,))
        usuario_existe = cursor.fetchone() is not None
        conexion.close()
        return usuario_existe






    # Manejo de roles
    def agregar_rol(self, nombre, permisos):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO roles (nombre, permisos) VALUES (?, ?)', (nombre, ",".join(permisos)))
        conexion.commit()
        conexion.close()

    def verificar_permiso(self, rol, permiso):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT permisos FROM roles WHERE nombre = ?', (rol,))
        permisos = cursor.fetchone()
        conexion.close()
        return permisos and permiso in permisos[0].split(',')
    
    def obtener_estudiantes(self):
        try:
            # Conexión a la base de datos
            conexion = self.get_db_connection()
            cursor = conexion.cursor()

            # Consulta para obtener a los estudiantes
            cursor.execute("SELECT id, nombre, email FROM usuarios WHERE rol = 'estudiante'")
            estudiantes = cursor.fetchall()

            # Cierre de la conexión
            conexion.close()

            # Retornar una lista de estudiantes estructurada
            return [{"id": e[0], "nombre": e[1], "email": e[2]} for e in estudiantes]

        except sqlite3.Error as e:
            # Manejo de errores específicos de SQLite
            return {"error": f"Error de base de datos: {str(e)}"}
        
        except Exception as e:
            # Manejo de otros errores
            return {"error": f"Error inesperado: {str(e)}"}





    # Manejo de notas
    def gestionar_notas(self, usuario_id, contenido):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO notas (contenido, usuario_id) VALUES (?, ?)', (contenido, usuario_id))
        conexion.commit()
        conexion.close()

    def obtener_notas_usuario(self, usuario_id):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT contenido FROM notas WHERE usuario_id = ?', (usuario_id,))
        notas = cursor.fetchall()
        conexion.close()
        # Retorna una lista de notas, o lista vacía si no hay notas
        return [{"contenido": nota[0]} for nota in notas] if notas else []
    

    def asignarNotaPorEmail(self, email, contenido):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
        usuario_data = cursor.fetchone()

        if usuario_data is None:
            conexion.close()
            return {"error": "Usuario no encontrado"}

        usuario_id = usuario_data[0]

        try:
            cursor.execute('INSERT INTO notas (contenido, usuario_id) VALUES (?, ?)', (contenido, usuario_id))
            conexion.commit()
            conexion.close()
            return {"success": "Nota asignada exitosamente"}
        except sqlite3.Error as e:
            # Manejo de errores específicos de SQLite
            conexion.close()
            return {"error": f"Error de base de datos: {str(e)}"}
        except Exception as e:
            # Manejo de cualquier otro error inesperado
            conexion.close()
            return {"error": f"Error inesperado: {str(e)}"}





    # Métodos de utilidad
    def verificar_tablas(self):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        conexion.close()
        print("Tablas en la base de datos:", tablas)

    def listar_tablas(self):
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        conexion.close()
        return tablas



    #multifactor
    # Método para habilitar MFA
    def habilitar_mfa(self, usuario_id):
    # Establecer conexión con la base de datos
        conexion = self.get_db_connection()
        cursor = conexion.cursor()
        
        try:
            # Obtener el usuario
            usuario = self.obtener_usuario_por_id(usuario_id)
            if not usuario:
                raise ValueError("Usuario no encontrado")

            # Generar el secreto MFA
            secret = pyotp.random_base32()
            print("Secreto generado:", secret)
            
            # Cifrar y asignar el secreto MFA
            clave_cifrada = usuario.cifrar_mfa(secret)
            print("Secreto cifrado:", clave_cifrada)
            print("Secreto descifrado:", usuario.descifrar_mfa())
            
            # Actualizar la base de datos con el secreto cifrado
            cursor.execute(
                'UPDATE usuarios SET mfa_secret = ? WHERE id = ?',
                (clave_cifrada, usuario_id)
            )
            conexion.commit()

            # Generar la URL para el QR Code
            totp = pyotp.TOTP(secret)
            qr_url = totp.provisioning_uri(name=f"user_{usuario_id}", issuer_name="SistemaNotas")

            return {"secret": secret, "qr_url": qr_url}

        except Exception as e:
            # Manejo de excepciones (opcional)
            raise e

        finally:
            # Asegurar el cierre de la conexión
            conexion.close()