from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import List, Optional


@dataclass
class Influencer:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    nombre: str = None
    plataforma: str = None
    seguidores: int = 0
    categoria: str = None
    activo: bool = True
    fecha_registro: datetime = field(default_factory=datetime.now)
    _eventos: List = field(default_factory=list, init=False)

    def agregar_evento(self, evento):
        self._eventos.append(evento)

    def limpiar_eventos(self):
        self._eventos.clear()

    def obtener_eventos(self):
        return self._eventos.copy()


@dataclass
class CampanaInfluencer:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    id_campana: uuid.UUID = None
    id_influencer: uuid.UUID = None
    id_marca: uuid.UUID = None
    nombre_campana: str = None
    estado: str = None
    fecha_asignacion: datetime = field(default_factory=datetime.now)
    fecha_inicio: Optional[datetime] = None
    presupuesto_asignado: float = 0.0
    _eventos: List = field(default_factory=list, init=False)

    def procesar_campana_creada(self, evento_data):
        self.id_campana = evento_data.get('id_campana')
        self.id_marca = evento_data.get('id_marca')
        self.nombre_campana = evento_data.get('nombre')
        self.estado = evento_data.get('estado')
        self.fecha_asignacion = datetime.fromtimestamp(
            evento_data.get('fecha_creacion', 0) / 1000)
        self.presupuesto_asignado = evento_data.get('presupuesto', 0.0)

    def procesar_campana_iniciada(self, evento_data):
        self.estado = evento_data.get('estado')
        self.fecha_inicio = datetime.fromtimestamp(
            evento_data.get('fecha_inicio', 0) / 1000)

    def asignar_influencer(self, id_influencer: uuid.UUID):
        self.id_influencer = id_influencer

    def agregar_evento(self, evento):
        self._eventos.append(evento)

    def limpiar_eventos(self):
        self._eventos.clear()

    def obtener_eventos(self):
        return self._eventos.copy()
