from sistema import SistemaNotas
if __name__ == "__main__":
    sistema = SistemaNotas()  # Crea las tablas
    #sistema.registrar_usuario(1, "Alice", "alice@example.com", "password123", "admin")
    email = "alice@example.com"
    clave = "password123"

    #print("es ", sistema.obtener_usuario_por_id(1).mfa_secret)


    # Llamada a la función de autenticación
    usuario = sistema.autenticar_usuario(email, clave)
    sistema.asignarNotaPorEmail("mapodsfadsaft", "13")
    #usuario2 = sistema.obtener_usuario_por_id(1)
    #print(usuario2.nombre)