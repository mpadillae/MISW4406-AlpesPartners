from pulsar.schema import *
from dataclasses import dataclass, field
from alpespartners.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearCampanaPayload(ComandoIntegracion):
    id_marca = String()

class ComandoCrearCampana(ComandoIntegracion):
    data = ComandoCrearCampanaPayload()