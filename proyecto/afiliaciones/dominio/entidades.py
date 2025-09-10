from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import List, Optional
from .objetos_valor import EstadoCampana, TipoCampana
from .eventos import CampanaCreada, CampanaIniciada


@dataclass
class Campana:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    id_marca: uuid.UUID = None
    nombre: str = None
    descripcion: str = None
    tipo: TipoCampana = None
    estado: EstadoCampana = EstadoCampana.CREADA
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    presupuesto: float = 0.0
    _eventos: List = field(default_factory=list, init=False)

    def iniciar_campana(self):
        if self.estado != EstadoCampana.CREADA:
            raise ValueError(
                "Solo se pueden iniciar campañas en estado CREADA")

        self.estado = EstadoCampana.INICIADA
        self.fecha_inicio = datetime.now()

        evento = CampanaIniciada(
            id_campana=self.id,
            id_marca=self.id_marca,
            estado=self.estado.value,
            fecha_inicio=self.fecha_inicio
        )
        self._eventos.append(evento)

    def agregar_evento(self, evento):
        self._eventos.append(evento)

    def limpiar_eventos(self):
        self._eventos.clear()

    def obtener_eventos(self):
        return self._eventos.copy()
