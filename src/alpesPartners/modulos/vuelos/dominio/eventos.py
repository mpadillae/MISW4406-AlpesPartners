from __future__ import annotations
from dataclasses import dataclass, field
from alpesPartners.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime


@dataclass
class ReservaCreada(EventoDominio):
    id_reserva: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
