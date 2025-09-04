from pulsar.schema import *
from alpespartners.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class CampanaCreadaPayload(Record):
    id_campana = String()
    id_marca = String()
    estado = String()
    fecha_creacion = Long()

class EventoCampanaCreada(EventoIntegracion):
    data = CampanaCreadaPayload()