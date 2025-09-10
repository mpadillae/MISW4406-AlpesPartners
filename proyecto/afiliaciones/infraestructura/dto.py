from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class CampanaDTO(BaseModel):
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
