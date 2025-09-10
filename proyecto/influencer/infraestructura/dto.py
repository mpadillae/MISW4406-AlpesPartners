from pydantic import BaseModel
from datetime import datetime
import uuid


class InfluencerDTO(BaseModel):
    id: uuid.UUID
    nombre: str
    plataforma: str
    seguidores: int
    categoria: str
    activo: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True


class CampanaInfluencerDTO(BaseModel):
    id: uuid.UUID
    id_campana: uuid.UUID
    id_influencer: uuid.UUID
    id_marca: uuid.UUID
    nombre_campana: str
    estado: str
    fecha_asignacion: datetime
    fecha_inicio: datetime = None
    presupuesto_asignado: float

    class Config:
        from_attributes = True
