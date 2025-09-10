from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class MarcaDTO(BaseModel):
    id: uuid.UUID
    id_marca: uuid.UUID
    nombre: str
    categoria: str
    fecha_creacion: datetime
    activa: bool

    class Config:
        from_attributes = True


class CampanaMarcaDTO(BaseModel):
    id: uuid.UUID
    id_campana: uuid.UUID
    id_marca: uuid.UUID
    nombre_campana: str
    estado: str
    fecha_creacion: datetime
    fecha_inicio: Optional[datetime] = None
    presupuesto: float

    class Config:
        from_attributes = True
