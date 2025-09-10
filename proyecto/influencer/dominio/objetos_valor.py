from enum import Enum
from dataclasses import dataclass


class PlataformaInfluencer(Enum):
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    FACEBOOK = "facebook"


class CategoriaInfluencer(Enum):
    MODA = "moda"
    TECNOLOGIA = "tecnologia"
    BELLEZA = "belleza"
    FITNESS = "fitness"
    VIAJES = "viajes"
    COMIDA = "comida"
    LIFESTYLE = "lifestyle"
    OTROS = "otros"


@dataclass(frozen=True)
class InformacionInfluencer:
    nombre: str
    plataforma: str
    seguidores: int
    categoria: str


@dataclass(frozen=True)
class DatosCampanaInfluencer:
    id_campana: str
    nombre: str
    estado: str
    presupuesto: float
