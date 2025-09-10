from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class EventoDominio:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_evento: datetime = field(default_factory=datetime.now)


@dataclass
class InfluencerAsignado(EventoDominio):
    id_campana: uuid.UUID = None
    id_influencer: uuid.UUID = None
    id_marca: uuid.UUID = None
    fecha_asignacion: datetime = None


@dataclass
class CampanaProcesada(EventoDominio):
    id_campana: uuid.UUID = None
    id_influencer: uuid.UUID = None
    id_marca: uuid.UUID = None
    nombre_campana: str = None
    estado: str = None
    fecha_procesamiento: datetime = None
