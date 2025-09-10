from typing import List, Dict, Any
import uuid
from .entidades import MetricasCampana, EventoTracking
from .repositorios import RepositorioMetricasCampana, RepositorioEventoTracking
from .eventos import MetricasActualizadas, EventoRegistrado


class ServicioTracking:
    def __init__(self, repositorio_metricas: RepositorioMetricasCampana, repositorio_eventos: RepositorioEventoTracking):
        self.repositorio_metricas = repositorio_metricas
        self.repositorio_eventos = repositorio_eventos

    def procesar_campana_creada(self, evento_data: dict) -> MetricasCampana:
        # Crear métricas de campaña
        metricas = MetricasCampana()
        metricas.procesar_campana_creada(evento_data)

        # Guardar en repositorio
        metricas_guardadas = self.repositorio_metricas.agregar(metricas)

        # Crear evento de dominio
        evento = EventoRegistrado(
            id_campana=metricas_guardadas.id_campana,
            tipo_evento="campana_creada",
            datos=evento_data,
            fecha_registro=metricas_guardadas.fecha_creacion
        )
        metricas_guardadas.agregar_evento(evento)

        return metricas_guardadas

    def procesar_campana_iniciada(self, evento_data: dict) -> MetricasCampana:
        # Buscar métricas existentes
        id_campana = uuid.UUID(evento_data.get('id_campana'))
        metricas = self.repositorio_metricas.obtener_por_id(id_campana)

        if metricas:
            metricas.procesar_campana_iniciada(evento_data)
            return self.repositorio_metricas.actualizar(metricas)

        return None

    def registrar_evento_tracking(self, id_campana: uuid.UUID, tipo_evento: str, datos: Dict[str, Any]) -> EventoTracking:
        # Crear evento de tracking
        evento = EventoTracking(
            id_campana=id_campana,
            tipo_evento=tipo_evento,
            datos=datos
        )

        # Guardar evento
        evento_guardado = self.repositorio_eventos.agregar(evento)

        # Actualizar métricas de la campaña
        metricas = self.repositorio_metricas.obtener_por_id(id_campana)
        if metricas:
            nuevas_metricas = self._calcular_metricas_desde_evento(
                tipo_evento, datos)
            metricas.actualizar_metricas(nuevas_metricas)
            self.repositorio_metricas.actualizar(metricas)

        return evento_guardado

    def _calcular_metricas_desde_evento(self, tipo_evento: str, datos: Dict[str, Any]) -> Dict[str, Any]:
        metricas = {}

        if tipo_evento == "vista":
            metricas["vistas"] = 1
        elif tipo_evento == "clic":
            metricas["clics"] = 1
        elif tipo_evento == "conversion":
            metricas["conversiones"] = 1
        elif tipo_evento == "engagement":
            metricas["engagement"] = datos.get("valor", 0.0)

        return metricas

    def obtener_metricas_campana(self, id_campana: uuid.UUID) -> MetricasCampana:
        return self.repositorio_metricas.obtener_por_id(id_campana)

    def obtener_metricas_por_marca(self, id_marca: uuid.UUID) -> List[MetricasCampana]:
        return self.repositorio_metricas.obtener_por_marca(id_marca)

    def obtener_eventos_campana(self, id_campana: uuid.UUID) -> List[EventoTracking]:
        return self.repositorio_eventos.obtener_por_campana(id_campana)
