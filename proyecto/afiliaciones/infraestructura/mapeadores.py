from dominio.entidades import Campana
from .dto import CampanaDTO


class MapeadorCampanaInfraestructura:
    @staticmethod
    def entidad_a_dto(campana: Campana) -> CampanaDTO:
        return CampanaDTO(
            id=campana.id,
            id_marca=campana.id_marca,
            nombre=campana.nombre,
            descripcion=campana.descripcion,
            tipo=campana.tipo.value if campana.tipo else "influencer",
            estado=campana.estado.value if campana.estado else "creada",
            fecha_creacion=campana.fecha_creacion,
            fecha_inicio=campana.fecha_inicio,
            fecha_fin=campana.fecha_fin,
            presupuesto=campana.presupuesto
        )

    @staticmethod
    def dto_a_entidad(dto: CampanaDTO) -> Campana:
        from dominio.objetos_valor import TipoCampana, EstadoCampana

        return Campana(
            id=dto.id,
            id_marca=dto.id_marca,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            tipo=TipoCampana(dto.tipo),
            estado=EstadoCampana(dto.estado),
            fecha_creacion=dto.fecha_creacion,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            presupuesto=dto.presupuesto
        )
