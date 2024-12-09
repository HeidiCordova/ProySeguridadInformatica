class Rol:
    def __init__(self, nombre, permisos):
        self.nombre = nombre
        self.permisos = permisos  # Lista de permisos asignados al rol

    def tiene_permiso(self, permiso):
        """Verifica si el rol tiene un permiso específico."""
        return permiso in self.permisos
