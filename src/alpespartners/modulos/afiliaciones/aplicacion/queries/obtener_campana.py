from alpespartners.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from alpespartners.seedwork.aplicacion.queries import ejecutar_query as query
from alpespartners.modulos.afiliaciones.infraestructura.repositorios import RepositorioCampanas
from dataclasses import dataclass
from .base import CampanaQueryBaseHandler
from alpespartners.modulos.afiliaciones.aplicacion.mapeadores import MapeadorCampana
import uuid

@dataclass
class ObtenerCampana(Query):
    id: str

class ObtenerCampanaHandler(CampanaQueryBaseHandler):

    def handle(self, query: ObtenerCampana) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampanas.__class__)
        campana = self.fabrica_afiliaciones.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorCampana())
        return QueryResultado(resultado=campana)

@query.register(ObtenerCampana)
def ejecutar_query_obtener_campana(query: ObtenerCampana):
    handler = ObtenerCampanaHandler()
    return handler.handle(query)
