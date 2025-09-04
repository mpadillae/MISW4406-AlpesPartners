""" Mapeadores para la capa de infrastructura del dominio de afiliaciones

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.modulos.afiliaciones.dominio.objetos_valor import *
from alpespartners.modulos.afiliaciones.dominio.entidades import Campana, Influencer, RedSocial
from .dto import Campana as CampanaDTO
from .dto import Influencer as InfluencerDTO

class MapeadorCampana(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def _procesar_influencers_dto(self, influencers_dto: list) -> list[Influencer]:
        influencers = []
        
        for inf_dto in influencers_dto:
            red_social = RedSocial(
                nombre=NombreRedSocial("Instagram"),
                enlace=EnlaceRedSocial("https://instagram.com/example"),
                numero_seguidores=NumeroSeguidores(inf_dto.seguidores),
                engagement_rate=EngagementRate(3.5)
            )
            
            influencer = Influencer(
                nombre=NombreInfluencer(inf_dto.nombre),
                email=EmailInfluencer(f"{inf_dto.nombre.lower().replace(' ', '')}@email.com"),
                categoria=CategoriaInfluencer.MODA,
                precio_por_post=PrecioPorPost(inf_dto.costo_por_post),
                ubicacion=UbicacionInfluencer("Madrid, España"),
                redes_sociales=[red_social]
            )
            influencers.append(influencer)

        return influencers

    def _procesar_influencers(self, influencers: list[Influencer]) -> list[InfluencerDTO]:
        influencers_dto = []

        for influencer in influencers:
            influencer_dto = InfluencerDTO()
            influencer_dto.nombre = influencer.nombre.nombre
            influencer_dto.red_social = "Instagram"
            influencer_dto.seguidores = influencer.redes_sociales[0].numero_seguidores.seguidores if influencer.redes_sociales else 0
            influencer_dto.costo_por_post = influencer.precio_por_post.precio
            influencers_dto.append(influencer_dto)

        return influencers_dto

    def obtener_tipo(self) -> type:
        return Campana.__class__

    def entidad_a_dto(self, entidad: Campana) -> CampanaDTO:
        
        campana_dto = CampanaDTO()
        campana_dto.fecha_creacion = entidad.fecha_creacion
        campana_dto.fecha_actualizacion = entidad.fecha_actualizacion
        campana_dto.id = str(entidad.id)
        campana_dto.nombre = entidad.nombre.nombre
        campana_dto.descripcion = entidad.descripcion.descripcion
        campana_dto.fecha_inicio = entidad.fecha_inicio.fecha_inicio
        campana_dto.fecha_fin = entidad.fecha_fin.fecha_fin
        campana_dto.presupuesto = entidad.presupuesto.monto

        influencers_dto = self._procesar_influencers(entidad.influencers)
        campana_dto.influencers = influencers_dto

        return campana_dto

    def dto_a_entidad(self, dto: CampanaDTO) -> Campana:
        campana = Campana(
            id=dto.id,
            nombre=NombreCampana(dto.nombre),
            descripcion=DescripcionCampana(dto.descripcion),
            fecha_inicio=FechaInicioCampana(dto.fecha_inicio),
            fecha_fin=FechaFinCampana(dto.fecha_fin),
            presupuesto=PresupuestoCampana(dto.presupuesto),
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion
        )
        
        campana.influencers = self._procesar_influencers_dto(dto.influencers)
        
        return campana