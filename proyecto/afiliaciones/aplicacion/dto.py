from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class CrearCampanaRequest(BaseModel):
    id_marca: uuid.UUID
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: str = Field(..., min_length=1, max_length=500)
    tipo: str = Field(...)
    presupuesto: float = Field(...)


class CampanaResponse(BaseModel):
    id: uuid.UUID
    id_marca: uuid.UUID
    nombre: str
    descripcion: str
    tipo: str
    estado: str
    fecha_creacion: datetime
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    presupuesto: float

    class Config:
        from_attributes = True


class IniciarCampanaRequest(BaseModel):
    id_campana: uuid.UUID


class CampanaListResponse(BaseModel):
    campanas: list[CampanaResponse]
    total: int
