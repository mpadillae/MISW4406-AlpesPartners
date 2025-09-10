from enum import Enum
from dataclasses import dataclass


class CategoriaMarca(Enum):
    MODA = "moda"
    TECNOLOGIA = "tecnologia"
    BELLEZA = "belleza"
    DEPORTES = "deportes"
    ALIMENTOS = "alimentos"
    OTROS = "otros"


@dataclass(frozen=True)
class InformacionMarca:
    nombre: str
    categoria: str
    descripcion: str


@dataclass(frozen=True)
class DatosCampana:
    id_campana: str
    nombre: str
    estado: str
    presupuesto: float
