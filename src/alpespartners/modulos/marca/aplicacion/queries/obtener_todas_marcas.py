from alpespartners.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
import uuid


class ObtenerTodasMarcas(Query):
    ...


class ObtenerTodasMarcasHandler(QueryHandler):

    def handle(self, query: Query) -> QueryResultado:
        ...
