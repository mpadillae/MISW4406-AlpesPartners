"""Objetos valor del dominio de afiliaciones

En este archivo usted encontrará los objetos valor del dominio de afiliaciones y marketing de influencers

"""

from __future__ import annotations

from dataclasses import dataclass, field
from alpespartners.seedwork.dominio.objetos_valor import ObjetoValor
from datetime import datetime
from enum import Enum


# Enumeraciones para el dominio de afiliaciones
class EstadoCampana(str, Enum):
    PENDIENTE = "Pendiente"
    ACTIVA = "Activa"
    PAUSADA = "Pausada"
    FINALIZADA = "Finalizada"
    CANCELADA = "Cancelada"


class TipoContenido(str, Enum):
    POST = "Post"
    STORY = "Story"
    REEL = "Reel"
    VIDEO = "Video"
    LIVE = "Live"
    IGTV = "IGTV"


class CategoriaInfluencer(str, Enum):
    MODA = "Moda"
    BELLEZA = "Belleza"
    FITNESS = "Fitness"
    VIAJES = "Viajes"
    TECNOLOGIA = "Tecnología"
    GASTRONOMIA = "Gastronomía"
    LIFESTYLE = "Lifestyle"
    DEPORTE = "Deporte"
    EDUCACION = "Educación"
    ENTRETENIMIENTO = "Entretenimiento"


class ObjetivoCampana(str, Enum):
    AWARENESS = "Awareness"
    ENGAGEMENT = "Engagement"
    CONVERSION = "Conversión"
    TRAFFIC = "Tráfico"
    REACH = "Alcance"
    BRANDING = "Branding"


# Objetos valor específicos del dominio
@dataclass(frozen=True)
class NombreCampana(ObjetoValor):
    valor: str

    def __post_init__(self):
        if not self.valor or len(self.valor.strip()) == 0:
            raise ValueError("El nombre de la campaña no puede estar vacío")
        if len(self.valor) > 100:
            raise ValueError("El nombre de la campaña no puede exceder 100 caracteres")


@dataclass(frozen=True)
class DescripcionCampana(ObjetoValor):
    valor: str

    def __post_init__(self):
        if not self.valor or len(self.valor.strip()) == 0:
            raise ValueError("La descripción de la campaña no puede estar vacía")
        if len(self.valor) > 1000:
            raise ValueError("La descripción no puede exceder 1000 caracteres")


@dataclass(frozen=True)
class PresupuestoCampana(ObjetoValor):
    valor: float

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El presupuesto no puede ser negativo")


@dataclass(frozen=True)
class FechaInicio(ObjetoValor):
    valor: datetime


@dataclass(frozen=True)
class FechaFin(ObjetoValor):
    valor: datetime


@dataclass(frozen=True)
class AudienciaObjetivo(ObjetoValor):
    valor: str

    def __post_init__(self):
        if not self.valor or len(self.valor.strip()) == 0:
            raise ValueError("La audiencia objetivo no puede estar vacía")


@dataclass(frozen=True)
class Hashtag(ObjetoValor):
    valor: str

    def __post_init__(self):
        if not self.valor.startswith('#'):
            raise ValueError("El hashtag debe comenzar con '#'")
        if len(self.valor) < 2:
            raise ValueError("El hashtag debe tener al menos 2 caracteres")


@dataclass(frozen=True)
class NombreInfluencer(ObjetoValor):
    valor: str

    def __post_init__(self):
        if not self.valor or len(self.valor.strip()) == 0:
            raise ValueError("El nombre del influencer no puede estar vacío")


@dataclass(frozen=True)
class EmailInfluencer(ObjetoValor):
    valor: str

    def __post_init__(self):
        if not self.valor or '@' not in self.valor:
            raise ValueError("Email del influencer inválido")


@dataclass(frozen=True)
class PrecioPorPost(ObjetoValor):
    valor: float

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El precio por post no puede ser negativo")


@dataclass(frozen=True)
class UbicacionInfluencer(ObjetoValor):
    valor: str


@dataclass(frozen=True)
class NombreRedSocial(ObjetoValor):
    valor: str

    def __post_init__(self):
        redes_permitidas = ['Instagram', 'TikTok', 'YouTube', 'Twitter', 'Facebook', 'LinkedIn']
        if self.valor not in redes_permitidas:
            raise ValueError(f"Red social no permitida. Debe ser una de: {redes_permitidas}")


@dataclass(frozen=True)
class EnlaceRedSocial(ObjetoValor):
    valor: str

    def __post_init__(self):
        if not self.valor.startswith(('http://', 'https://')):
            raise ValueError("El enlace debe comenzar con http:// o https://")


@dataclass(frozen=True)
class NumeroSeguidores(ObjetoValor):
    valor: int

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El número de seguidores no puede ser negativo")


@dataclass(frozen=True)
class EngagementRate(ObjetoValor):
    valor: float

    def __post_init__(self):
        if self.valor < 0 or self.valor > 100:
            raise ValueError("El engagement rate debe estar entre 0 y 100")


@dataclass(frozen=True)
class NombreMetrica(ObjetoValor):
    valor: str

    def __post_init__(self):
        metricas_permitidas = ['Views', 'Likes', 'Shares', 'Comments', 'Clicks', 'Saves', 'Reach', 'Impressions']
        if self.valor not in metricas_permitidas:
            raise ValueError(f"Métrica no permitida. Debe ser una de: {metricas_permitidas}")


@dataclass(frozen=True)
class ValorMetrica(ObjetoValor):
    valor: int

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El valor de la métrica no puede ser negativo")


@dataclass(frozen=True)
class FechaMedicion(ObjetoValor):
    valor: datetime


@dataclass(frozen=True)
class DescripcionContenido(ObjetoValor):
    valor: str

    def __post_init__(self):
        if not self.valor or len(self.valor.strip()) == 0:
            raise ValueError("La descripción del contenido no puede estar vacía")


@dataclass(frozen=True)
class UrlContenido(ObjetoValor):
    valor: str

    def __post_init__(self):
        if not self.valor.startswith(('http://', 'https://')):
            raise ValueError("La URL del contenido debe comenzar con http:// o https://")


@dataclass(frozen=True)
class FechaPublicacion(ObjetoValor):
    valor: datetime


# Objetos valor complejos
@dataclass(frozen=True)
class RedSocial(ObjetoValor):
    nombre: NombreRedSocial
    enlace: EnlaceRedSocial
    numero_seguidores: NumeroSeguidores
    engagement_rate: EngagementRate


@dataclass(frozen=True)
class Influencer(ObjetoValor):
    nombre: NombreInfluencer
    email: EmailInfluencer
    categoria: CategoriaInfluencer
    precio_por_post: PrecioPorPost
    ubicacion: UbicacionInfluencer
    redes_sociales: list[RedSocial] = field(default_factory=list)

    def calcular_alcance_total(self) -> int:
        return sum(red.numero_seguidores.valor for red in self.redes_sociales)


@dataclass(frozen=True)
class Metrica(ObjetoValor):
    nombre: NombreMetrica
    valor: ValorMetrica
    fecha_medicion: FechaMedicion


@dataclass(frozen=True)
class Contenido(ObjetoValor):
    tipo: TipoContenido
    descripcion: DescripcionContenido
    url_contenido: UrlContenido
    fecha_publicacion: FechaPublicacion
    influencer: Influencer
    metricas: list[Metrica] = field(default_factory=list)
