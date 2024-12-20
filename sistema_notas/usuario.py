import bcrypt
from cryptography.fernet import Fernet

# Clave de cifrado segura
FERNET_KEY = Fernet.generate_key()
cipher_suite = Fernet(FERNET_KEY)

class Usuario:
    def __init__(self, id, nombre, email, clave, rol, mfa_secret=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.clave = self.cifrar_clave(clave)
        self.rol = rol
        self.mfa_secret = self.cifrar_mfa_secret(mfa_secret) if mfa_secret else None

    def cifrar_clave(self, clave):
        """Cifra la clave del usuario usando bcrypt."""
        return bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())

    def verificar_clave(self, clave):
        """Verifica si la clave dada coincide con la clave cifrada."""
        return bcrypt.checkpw(clave.encode('utf-8'), self.clave)
    
    def cifrar_mfa_secret(self, mfa_secret):
        """Cifra el secreto MFA usando Fernet."""
        return cipher_suite.encrypt(mfa_secret.encode('utf-8'))

    def descifrar_mfa_secret(self):
        """Descifra el secreto MFA usando Fernet."""
        if self.mfa_secret:
            return cipher_suite.decrypt(self.mfa_secret).decode('utf-8')
        return None
