from dominio.entidades import Influencer, CampanaInfluencer
from .dto import InfluencerDTO, CampanaInfluencerDTO


class MapeadorInfluencerInfraestructura:
    @staticmethod
    def entidad_a_dto(influencer: Influencer) -> InfluencerDTO:
        return InfluencerDTO(
            id=influencer.id,
            nombre=influencer.nombre,
            plataforma=influencer.plataforma,
            seguidores=influencer.seguidores,
            categoria=influencer.categoria,
            activo=influencer.activo,
            fecha_registro=influencer.fecha_registro
        )

    @staticmethod
    def dto_a_entidad(dto: InfluencerDTO) -> Influencer:
        return Influencer(
            id=dto.id,
            nombre=dto.nombre,
            plataforma=dto.plataforma,
            seguidores=dto.seguidores,
            categoria=dto.categoria,
            activo=dto.activo,
            fecha_registro=dto.fecha_registro
        )


class MapeadorCampanaInfluencerInfraestructura:
    @staticmethod
    def entidad_a_dto(campana: CampanaInfluencer) -> CampanaInfluencerDTO:
        return CampanaInfluencerDTO(
            id=campana.id,
            id_campana=campana.id_campana,
            id_influencer=campana.id_influencer,
            id_marca=campana.id_marca,
            nombre_campana=campana.nombre_campana,
            estado=campana.estado,
            fecha_asignacion=campana.fecha_asignacion,
            fecha_inicio=campana.fecha_inicio,
            presupuesto_asignado=campana.presupuesto_asignado
        )

    @staticmethod
    def dto_a_entidad(dto: CampanaInfluencerDTO) -> CampanaInfluencer:
        return CampanaInfluencer(
            id=dto.id,
            id_campana=dto.id_campana,
            id_influencer=dto.id_influencer,
            id_marca=dto.id_marca,
            nombre_campana=dto.nombre_campana,
            estado=dto.estado,
            fecha_asignacion=dto.fecha_asignacion,
            fecha_inicio=dto.fecha_inicio,
            presupuesto_asignado=dto.presupuesto_asignado
        )
