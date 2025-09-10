from dominio.entidades import MetricasCampana, EventoTracking
from .dto import MetricasCampanaDTO, EventoTrackingDTO


class MapeadorMetricasCampanaInfraestructura:
    @staticmethod
    def entidad_a_dto(metricas: MetricasCampana) -> MetricasCampanaDTO:
        return MetricasCampanaDTO(
            id=metricas.id,
            id_campana=metricas.id_campana,
            id_marca=metricas.id_marca,
            nombre_campana=metricas.nombre_campana,
            estado=metricas.estado,
            fecha_creacion=metricas.fecha_creacion,
            fecha_inicio=metricas.fecha_inicio,
            presupuesto=metricas.presupuesto,
            metricas=metricas.metricas
        )

    @staticmethod
    def dto_a_entidad(dto: MetricasCampanaDTO) -> MetricasCampana:
        return MetricasCampana(
            id=dto.id,
            id_campana=dto.id_campana,
            id_marca=dto.id_marca,
            nombre_campana=dto.nombre_campana,
            estado=dto.estado,
            fecha_creacion=dto.fecha_creacion,
            fecha_inicio=dto.fecha_inicio,
            presupuesto=dto.presupuesto,
            metricas=dto.metricas
        )


class MapeadorEventoTrackingInfraestructura:
    @staticmethod
    def entidad_a_dto(evento: EventoTracking) -> EventoTrackingDTO:
        return EventoTrackingDTO(
            id=evento.id,
            id_campana=evento.id_campana,
            tipo_evento=evento.tipo_evento,
            datos=evento.datos,
            fecha_evento=evento.fecha_evento
        )

    @staticmethod
    def dto_a_entidad(dto: EventoTrackingDTO) -> EventoTracking:
        return EventoTracking(
            id=dto.id,
            id_campana=dto.id_campana,
            tipo_evento=dto.tipo_evento,
            datos=dto.datos,
            fecha_evento=dto.fecha_evento
        )
