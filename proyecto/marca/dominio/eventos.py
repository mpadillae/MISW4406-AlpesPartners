from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class EventoDominio:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_evento: datetime = field(default_factory=datetime.now)


@dataclass
class CampanaProcesada(EventoDominio):
    id_campana: uuid.UUID = None
    id_marca: uuid.UUID = None
    nombre_campana: str = None
    estado: str = None
    fecha_procesamiento: datetime = None


@dataclass
class MarcaActualizada(EventoDominio):
    id_marca: uuid.UUID = None
    nombre: str = None
    categoria: str = None
    fecha_actualizacion: datetime = None
