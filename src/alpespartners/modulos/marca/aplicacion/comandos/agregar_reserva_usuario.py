from alpespartners.seedwork.aplicacion.comandos import Comando, ComandoHandler    

class AgregarCampanaMarca(Comando):
    id_marca: uuid.UUID
    id_campana: uuid.UUID

class AgregarCampanaMarcaHandler(ComandoHandler):
    ...