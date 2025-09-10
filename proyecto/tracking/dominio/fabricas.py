from .entidades import MetricasCampana, EventoTracking
from .objetos_valor import TipoEventoTracking
import uuid


class FabricaMetricasCampana:
    @staticmethod
    def crear_metricas_campana(evento_data: dict) -> MetricasCampana:
        metricas = MetricasCampana()
        metricas.procesar_campana_creada(evento_data)
        return metricas


class FabricaEventoTracking:
    @staticmethod
    def crear_evento_tracking(id_campana: uuid.UUID, tipo_evento: str, datos: dict) -> EventoTracking:
        return EventoTracking(
            id_campana=id_campana,
            tipo_evento=tipo_evento,
            datos=datos
        )
