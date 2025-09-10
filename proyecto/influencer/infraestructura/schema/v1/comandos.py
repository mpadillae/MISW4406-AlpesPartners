from pulsar.schema import *


class ComandoIntegracion(Record):
    id = String()
    time = Long()
    ingestion = Long()
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()


class CrearCampanaPayload(Record):
    id_marca = String()
    nombre = String()
    descripcion = String()
    tipo = String()
    presupuesto = Double()


class ComandoCrearCampana(ComandoIntegracion):
    data = CrearCampanaPayload()


class IniciarCampanaPayload(Record):
    id_campana = String()


class ComandoIniciarCampana(ComandoIntegracion):
    data = IniciarCampanaPayload()
