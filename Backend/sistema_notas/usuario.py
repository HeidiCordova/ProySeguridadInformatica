import bcrypt
from cryptography.fernet import Fernet
import os

# Ruta del archivo donde se almacena la clave
CLAVE_PATH = "clave_fernet.key"

# Función para cargar o generar la clave
def cargar_o_generar_clave():
    if os.path.exists(CLAVE_PATH):
        with open(CLAVE_PATH, "rb") as archivo_clave:
            return archivo_clave.read()
    else:
        clave = Fernet.generate_key()
        with open(CLAVE_PATH, "wb") as archivo_clave:
            archivo_clave.write(clave)
        return clave


FERNET_KEY = cargar_o_generar_clave()
CIFRADOR_GLOBAL = Fernet(FERNET_KEY)

class Usuario:
    def __init__(self, id, nombre, email, clave, rol, mfa_secret=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.clave = self.cifrar_clave(clave)
        self.rol = rol
        self.mfa_secret = mfa_secret

    def cifrar_clave(self, clave):
        """Cifra la clave del usuario usando bcrypt."""
        return bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())

    def verificar_clave(self, clave):
        """Verifica si la clave dada coincide con la clave cifrada."""
        return bcrypt.checkpw(clave.encode('utf-8'), self.clave)

    def cifrar_mfa(self, mfa_secreto):
        """Cifra el secreto MFA usando la clave constante de la aplicación."""
        self.mfa_secret = CIFRADOR_GLOBAL.encrypt(mfa_secreto.encode('utf-8')).decode('utf-8')
        return self.mfa_secret

    def descifrar_mfa(self):
        """Descifra el secreto MFA usando la clave constante de la aplicación."""
        if self.mfa_secret:
            return CIFRADOR_GLOBAL.decrypt(self.mfa_secret.encode('utf-8')).decode('utf-8')
        return None

    
