from __future__ import annotations
from dataclasses import dataclass, field
from alpespartners.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
import uuid


@dataclass
class CampanaCreada(EventoDominio):
    id_campana: uuid.UUID = None
    id_marca: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
