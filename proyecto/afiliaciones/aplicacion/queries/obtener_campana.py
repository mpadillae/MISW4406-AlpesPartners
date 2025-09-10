from dataclasses import dataclass
import uuid
from .base import Query


@dataclass
class ObtenerCampana(Query):
    id_campana: uuid.UUID


@dataclass
class ObtenerTodasCampanas(Query):
    pass
