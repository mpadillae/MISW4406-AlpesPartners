from alpespartners.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
import uuid


class ObtenerMarca(Query):
    listing_id: uuid.UUID


class ObtenerMarcaHandler(QueryHandler):

    def handle(self, query: Query) -> QueryResultado:
        ...
