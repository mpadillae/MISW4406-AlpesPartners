from dataclasses import dataclass, field
from alpespartners.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class RedSocialDTO(DTO):
    nombre: str
    enlace: str
    numero_seguidores: int
    engagement_rate: float

@dataclass(frozen=True)
class InfluencerDTO(DTO):
    nombre: str
    email: str
    telefono: str
    categoria: str
    precio_por_post: float
    redes_sociales: list[RedSocialDTO]
    ubicacion: str

@dataclass(frozen=True)
class MetricaDTO(DTO):
    nombre: str
    valor: int
    fecha_medicion: str

@dataclass(frozen=True)
class ContenidoDTO(DTO):
    tipo: str
    descripcion: str
    url_contenido: str
    fecha_publicacion: str
    influencer: InfluencerDTO
    metricas: list[MetricaDTO]

@dataclass(frozen=True)
class CampanaDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    descripcion: str = field(default_factory=str)
    fecha_inicio: str = field(default_factory=str)
    fecha_fin: str = field(default_factory=str)
    presupuesto: float = field(default_factory=float)
    objetivo: str = field(default_factory=str)
    audiencia_objetivo: str = field(default_factory=str)
    hashtags: list[str] = field(default_factory=list)
    influencers: list[InfluencerDTO] = field(default_factory=list)
    contenidos: list[ContenidoDTO] = field(default_factory=list)