from pulsar.schema import *


class EventoIntegracion(Record):
    id = String()
    time = Long()
    ingestion = Long()
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()


class CampanaCreadaPayload(Record):
    id_campana = String()
    id_marca = String()
    nombre = String()
    descripcion = String()
    tipo = String()
    estado = String()
    fecha_creacion = Long()
    presupuesto = Double()


class EventoCampanaCreada(EventoIntegracion):
    data = CampanaCreadaPayload()


class CampanaIniciadaPayload(Record):
    id_campana = String()
    id_marca = String()
    estado = String()
    fecha_inicio = Long()


class EventoCampanaIniciada(EventoIntegracion):
    data = CampanaIniciadaPayload()
