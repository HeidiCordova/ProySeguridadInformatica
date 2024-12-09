import bcrypt

class Usuario:
    def __init__(self, id, nombre, email, clave, rol):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.clave = self.cifrar_clave(clave)
        self.rol = rol

    def cifrar_clave(self, clave):
        """Cifra la clave del usuario usando bcrypt."""
        return bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())

    def verificar_clave(self, clave):
        """Verifica si una clave dada coincide con la clave cifrada."""
        return bcrypt.checkpw(clave.encode('utf-8'), self.clave)