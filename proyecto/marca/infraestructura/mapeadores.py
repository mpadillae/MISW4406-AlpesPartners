from dominio.entidades import Marca, CampanaMarca
from .dto import MarcaDTO, CampanaMarcaDTO


class MapeadorMarcaInfraestructura:
    @staticmethod
    def entidad_a_dto(marca: Marca) -> MarcaDTO:
        return MarcaDTO(
            id=marca.id,
            id_marca=marca.id_marca,
            nombre=marca.nombre,
            categoria=marca.categoria,
            fecha_creacion=marca.fecha_creacion,
            activa=marca.activa
        )

    @staticmethod
    def dto_a_entidad(dto: MarcaDTO) -> Marca:
        return Marca(
            id=dto.id,
            id_marca=dto.id_marca,
            nombre=dto.nombre,
            categoria=dto.categoria,
            fecha_creacion=dto.fecha_creacion,
            activa=dto.activa
        )


class MapeadorCampanaMarcaInfraestructura:
    @staticmethod
    def entidad_a_dto(campana: CampanaMarca) -> CampanaMarcaDTO:
        return CampanaMarcaDTO(
            id=campana.id,
            id_campana=campana.id_campana,
            id_marca=campana.id_marca,
            nombre_campana=campana.nombre_campana,
            estado=campana.estado,
            fecha_creacion=campana.fecha_creacion,
            fecha_inicio=campana.fecha_inicio,
            presupuesto=campana.presupuesto
        )

    @staticmethod
    def dto_a_entidad(dto: CampanaMarcaDTO) -> CampanaMarca:
        return CampanaMarca(
            id=dto.id,
            id_campana=dto.id_campana,
            id_marca=dto.id_marca,
            nombre_campana=dto.nombre_campana,
            estado=dto.estado,
            fecha_creacion=dto.fecha_creacion,
            fecha_inicio=dto.fecha_inicio,
            presupuesto=dto.presupuesto
        )
