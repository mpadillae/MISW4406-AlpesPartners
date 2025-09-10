class InfraestructuraExcepcion(Exception):
    pass


class ErrorConexionBaseDatos(InfraestructuraExcepcion):
    def __init__(self, mensaje: str):
        super().__init__(f"Error de conexión a la base de datos: {mensaje}")


class ErrorConsumoEvento(InfraestructuraExcepcion):
    def __init__(self, mensaje: str):
        super().__init__(f"Error consumiendo evento: {mensaje}")
