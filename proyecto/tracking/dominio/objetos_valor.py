from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any


class TipoEventoTracking(Enum):
    VISTA = "vista"
    CLIC = "clic"
    CONVERSION = "conversion"
    ENGAGEMENT = "engagement"
    COMPARTIR = "compartir"
    COMENTARIO = "comentario"


class EstadoMetricas(Enum):
    INICIAL = "inicial"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    PAUSADA = "pausada"


@dataclass(frozen=True)
class DatosMetricas:
    vistas: int
    clics: int
    conversiones: int
    engagement: float
    costo_por_clic: float
    roi: float


@dataclass(frozen=True)
class DatosEvento:
    tipo: str
    datos: Dict[str, Any]
    timestamp: int
