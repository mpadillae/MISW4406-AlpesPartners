from enum import Enum
from dataclasses import dataclass
from typing import Optional


class EstadoCampana(Enum):
    CREADA = "creada"
    INICIADA = "iniciada"
    EN_PROGRESO = "en_progreso"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"


class TipoCampana(Enum):
    INFLUENCER = "influencer"
    AFILIADO = "afiliado"
    MIXTA = "mixta"


@dataclass(frozen=True)
class InformacionCampana:
    nombre: str
    descripcion: str
    presupuesto: float
    duracion_dias: int


@dataclass(frozen=True)
class DatosMarca:
    id_marca: str
    nombre: str
    categoria: str
