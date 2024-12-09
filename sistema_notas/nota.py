from cryptography.fernet import Fernet

class Nota:
    def __init__(self, id, contenido, propietario):
        self.id = id
        self.contenido = contenido
        self.propietario = propietario
        self.clave_cifrado = Fernet.generate_key()
        self.cifrador = Fernet(self.clave_cifrado)

    def cifrar_nota(self):
        """Cifra el contenido de la nota."""
        self.contenido = self.cifrador.encrypt(self.contenido.encode('utf-8')).decode('utf-8')

    def descifrar_nota(self):
        """Descifra el contenido de la nota."""
        self.contenido = self.cifrador.decrypt(self.contenido.encode('utf-8')).decode('utf-8')