import pytest
from sistema_notas.sistema import SistemaNotas

@pytest.fixture
def sistema():
    sistema = SistemaNotas(":memory:")  # Base de datos en memoria
    print(sistema.listar_tablas())  # Verifica si las tablas existen
    sistema.agregar_rol("admin", ["crear_usuario", "gestionar_notas"])
    sistema.agregar_rol("profesor", ["ver_notas", "editar_notas"])
    sistema.agregar_rol("estudiante", ["ver_notas", "crear_notas"])
    sistema.registrar_usuario(1, "Admin", "admin@example.com", "adminpass", "admin")
    sistema.registrar_usuario(2, "Profesor", "profesor@example.com", "profpass", "profesor")
    sistema.registrar_usuario(3, "Estudiante", "estudiante@example.com", "studpass", "estudiante")
    return sistema



def test_autenticacion_usuario(sistema):
    # Prueba de autenticación exitosa
    usuario = sistema.autenticar_usuario("admin@example.com", "adminpass")
    assert usuario is not None
    assert usuario.rol == "admin"

    # Prueba de autenticación fallida
    usuario_invalido = sistema.autenticar_usuario("admin@example.com", "wrongpass")
    assert usuario_invalido is None

def test_permisos_admin(sistema):
    usuario = sistema.autenticar_usuario("admin@example.com", "adminpass")
    assert usuario.rol == "admin"

    # El admin puede gestionar notas
    try:
        sistema.gestionar_notas(usuario.id, "Nota creada por Admin")
    except Exception as e:
        pytest.fail(f"El admin no debería fallar al gestionar notas: {e}")

def test_permisos_profesor(sistema):
    usuario = sistema.autenticar_usuario("profesor@example.com", "profpass")
    assert usuario.rol == "profesor"

    # El profesor no debería tener permiso para crear nuevas notas
    with pytest.raises(Exception):
        sistema.gestionar_notas(usuario.id, "Nota creada por Profesor")

def test_permisos_estudiante(sistema):
    usuario = sistema.autenticar_usuario("estudiante@example.com", "studpass")
    assert usuario.rol == "estudiante"

    # El estudiante puede crear y ver sus propias notas
    try:
        sistema.gestionar_notas(usuario.id, "Nota creada por Estudiante")
    except Exception as e:
        pytest.fail(f"El estudiante no debería fallar al crear notas: {e}")
