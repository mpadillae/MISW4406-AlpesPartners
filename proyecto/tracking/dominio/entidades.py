from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import List, Optional, Dict, Any


@dataclass
class MetricasCampana:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    id_campana: uuid.UUID = None
    id_marca: uuid.UUID = None
    nombre_campana: str = None
    estado: str = None
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_inicio: Optional[datetime] = None
    presupuesto: float = 0.0
    metricas: Dict[str, Any] = field(default_factory=dict)
    _eventos: List = field(default_factory=list, init=False)

    def procesar_campana_creada(self, evento_data):
        self.id_campana = evento_data.get('id_campana')
        self.id_marca = evento_data.get('id_marca')
        self.nombre_campana = evento_data.get('nombre')
        self.estado = evento_data.get('estado')
        self.fecha_creacion = datetime.fromtimestamp(
            evento_data.get('fecha_creacion', 0) / 1000)
        self.presupuesto = evento_data.get('presupuesto', 0.0)

        # Inicializar métricas básicas
        self.metricas = {
            "vistas": 0,
            "clics": 0,
            "conversiones": 0,
            "engagement": 0.0,
            "costo_por_clic": 0.0,
            "roi": 0.0
        }

    def procesar_campana_iniciada(self, evento_data):
        self.estado = evento_data.get('estado')
        self.fecha_inicio = datetime.fromtimestamp(
            evento_data.get('fecha_inicio', 0) / 1000)

    def actualizar_metricas(self, nuevas_metricas: Dict[str, Any]):
        self.metricas.update(nuevas_metricas)
        self._calcular_metricas_derivadas()

    def _calcular_metricas_derivadas(self):
        # Calcular ROI
        if self.presupuesto > 0 and self.metricas.get('conversiones', 0) > 0:
            self.metricas['roi'] = (
                self.metricas['conversiones'] * 100) / self.presupuesto

        # Calcular costo por clic
        if self.metricas.get('clics', 0) > 0:
            self.metricas['costo_por_clic'] = self.presupuesto / \
                self.metricas['clics']

    def agregar_evento(self, evento):
        self._eventos.append(evento)

    def limpiar_eventos(self):
        self._eventos.clear()

    def obtener_eventos(self):
        return self._eventos.copy()


@dataclass
class EventoTracking:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    id_campana: uuid.UUID = None
    tipo_evento: str = None
    datos: Dict[str, Any] = field(default_factory=dict)
    fecha_evento: datetime = field(default_factory=datetime.now)
    _eventos: List = field(default_factory=list, init=False)

    def agregar_evento(self, evento):
        self._eventos.append(evento)

    def limpiar_eventos(self):
        self._eventos.clear()

    def obtener_eventos(self):
        return self._eventos.copy()

    def procesar_campana_creada(self, evento_data):
        self.id_campana = evento_data.get('id_campana')
        self.tipo_evento = evento_data.get('tipo_evento')
        self.datos = evento_data.get('datos')
        self.fecha_evento = datetime.fromtimestamp(
            evento_data.get('fecha_evento', 0) / 1000)
