from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class EventoDominio:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_evento: datetime = field(default_factory=datetime.now)


@dataclass
class CampanaCreada(EventoDominio):
    id_campana: uuid.UUID = None
    id_marca: uuid.UUID = None
    nombre: str = None
    descripcion: str = None
    tipo: str = None
    estado: str = None
    fecha_creacion: datetime = None
    presupuesto: float = 0.0


@dataclass
class CampanaIniciada(EventoDominio):
    id_campana: uuid.UUID = None
    id_marca: uuid.UUID = None
    estado: str = None
    fecha_inicio: datetime = None
