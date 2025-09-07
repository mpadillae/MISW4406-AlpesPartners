from alpespartners.seedwork.aplicacion.comandos import Comando, ComandoHandler


class RegistrarMarca(Comando):
    nombres: str
    apellidos: str
    email: str
    password: str
    es_empresarial: bool


class RegistrarMarcaHandler(ComandoHandler):
    ...
