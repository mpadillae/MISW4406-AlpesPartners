from alpespartners.seedwork.aplicacion.queries import QueryHandler
from alpespartners.modulos.afiliaciones.infraestructura.fabricas import FabricaRepositorio
from alpespartners.modulos.afiliaciones.dominio.fabricas import FabricaAfiliaciones

class CampanaQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_afiliaciones: FabricaAfiliaciones = FabricaAfiliaciones()

    @property    
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_afiliaciones(self):
        return self._fabrica_afiliaciones    