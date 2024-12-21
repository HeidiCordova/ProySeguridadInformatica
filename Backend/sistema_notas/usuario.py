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
        """Cifra y asigna el secreto MFA usando Fernet."""
        if isinstance(mfa_secret, bytes):
            mfa_secret = mfa_secret.decode('utf-8')  # Asegura que sea str
        
        clave_cifrada = cipher_suite.encrypt(mfa_secret.encode('utf-8'))
        self.mfa_secret = clave_cifrada  # Asigna directamente
        return clave_cifrada

    def descifrar_mfa_secret(self):
        """Descifra el secreto MFA usando Fernet."""
        if self.mfa_secret:
            return cipher_suite.decrypt(self.mfa_secret).decode('utf-8')
        return None
    
    @classmethod
    def from_db_row(cls, row):
        """
        Constructor alternativo que permite crear un objeto Usuario
        desde una fila de base de datos.
        """
        id, nombre, email, clave, rol, mfa_secret = row
        return cls(
            id=id,
            nombre=nombre,
            email=email,
            clave=clave.encode('utf-8'),
            rol=rol,
            mfa_secret=mfa_secret.encode('utf-8') if mfa_secret else None
        )
