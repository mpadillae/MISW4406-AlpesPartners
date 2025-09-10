from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class MetricasCampanaDTO(BaseModel):
    id: uuid.UUID
    id_campana: uuid.UUID
    id_marca: uuid.UUID
    nombre_campana: str
    estado: str
    fecha_creacion: datetime
    fecha_inicio: Optional[datetime] = None
    presupuesto: float
    metricas: Dict[str, Any]

    class Config:
        from_attributes = True


class EventoTrackingDTO(BaseModel):
    id: uuid.UUID
    id_campana: uuid.UUID
    tipo_evento: str
    datos: Dict[str, Any]
    fecha_evento: datetime

    class Config:
        from_attributes = True
