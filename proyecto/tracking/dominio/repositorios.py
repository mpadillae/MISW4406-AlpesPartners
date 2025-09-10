from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import uuid
from .entidades import MetricasCampana, EventoTracking


class RepositorioMetricasCampana(ABC):
    @abstractmethod
    def obtener_por_id(self, id_campana: uuid.UUID) -> Optional[MetricasCampana]:
        pass

    @abstractmethod
    def obtener_por_marca(self, id_marca: uuid.UUID) -> List[MetricasCampana]:
        pass

    @abstractmethod
    def obtener_todas(self) -> List[MetricasCampana]:
        pass

    @abstractmethod
    def agregar(self, metricas: MetricasCampana) -> MetricasCampana:
        pass

    @abstractmethod
    def actualizar(self, metricas: MetricasCampana) -> MetricasCampana:
        pass


class RepositorioEventoTracking(ABC):
    @abstractmethod
    def obtener_por_campana(self, id_campana: uuid.UUID) -> List[EventoTracking]:
        pass

    @abstractmethod
    def obtener_por_tipo(self, tipo_evento: str) -> List[EventoTracking]:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[EventoTracking]:
        pass

    @abstractmethod
    def agregar(self, evento: EventoTracking) -> EventoTracking:
        pass
