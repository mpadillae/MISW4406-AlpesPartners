from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import Dict, Any


@dataclass
class EventoDominio:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_evento: datetime = field(default_factory=datetime.now)


@dataclass
class MetricasActualizadas(EventoDominio):
    id_campana: uuid.UUID = None
    metricas: Dict[str, Any] = None
    fecha_actualizacion: datetime = None


@dataclass
class EventoRegistrado(EventoDominio):
    id_campana: uuid.UUID = None
    tipo_evento: str = None
    datos: Dict[str, Any] = None
    fecha_registro: datetime = None
