from alpespartners.seedwork.aplicacion.dto import Mapeador as AppMap
from alpespartners.seedwork.dominio.repositorios import Mapeador as RepMap
from alpespartners.modulos.afiliaciones.dominio.entidades import Campana, Influencer as InfluencerEntity, RedSocial as RedSocialEntity, Contenido
from alpespartners.modulos.afiliaciones.dominio.objetos_valor import *
from .dto import CampanaDTO, InfluencerDTO, RedSocialDTO, ContenidoDTO, MetricaDTO
from datetime import datetime


class MapeadorCampanaDTOJson(AppMap):

    def _procesar_influencer(self, influencer: dict) -> InfluencerDTO:
        redes_sociales = []
        for red in influencer.get('redes_sociales', []):
            red_dto = RedSocialDTO(
                nombre=red.get('nombre'),
                enlace=red.get('enlace'),
                numero_seguidores=red.get('numero_seguidores'),
                engagement_rate=red.get('engagement_rate')
            )
            redes_sociales.append(red_dto)

        return InfluencerDTO(
            nombre=influencer.get('nombre'),
            email=influencer.get('email'),
            telefono=influencer.get('telefono', ''),
            categoria=influencer.get('categoria'),
            precio_por_post=influencer.get('precio_por_post'),
            redes_sociales=redes_sociales,
            ubicacion=influencer.get('ubicacion')
        )

    def externo_a_dto(self, externo: dict) -> CampanaDTO:
        influencers = []
        for inf in externo.get('influencers', []):
            influencers.append(self._procesar_influencer(inf))

        return CampanaDTO(
            fecha_creacion=externo.get('fecha_creacion', ''),
            fecha_actualizacion=externo.get('fecha_actualizacion', ''),
            id=externo.get('id', ''),
            nombre=externo.get('nombre', ''),
            descripcion=externo.get('descripcion', ''),
            fecha_inicio=externo.get('fecha_inicio', ''),
            fecha_fin=externo.get('fecha_fin', ''),
            presupuesto=externo.get('presupuesto', 0.0),
            objetivo=externo.get('objetivo', ''),
            audiencia_objetivo=externo.get('audiencia_objetivo', ''),
            hashtags=externo.get('hashtags', []),
            influencers=influencers
        )

    def dto_a_externo(self, dto: CampanaDTO) -> dict:
        return {
            'fecha_creacion': dto.fecha_creacion,
            'fecha_actualizacion': dto.fecha_actualizacion,
            'id': dto.id,
            'nombre': dto.nombre,
            'descripcion': dto.descripcion,
            'fecha_inicio': dto.fecha_inicio,
            'fecha_fin': dto.fecha_fin,
            'presupuesto': dto.presupuesto,
            'objetivo': dto.objetivo,
            'audiencia_objetivo': dto.audiencia_objetivo,
            'hashtags': dto.hashtags,
            'influencers': [inf.__dict__ for inf in dto.influencers]
        }


class MapeadorCampana(RepMap):

    def _procesar_influencer_dto(self, influencer_dto: InfluencerDTO) -> InfluencerEntity:
        redes_sociales = []
        for red_dto in influencer_dto.redes_sociales:
            red = RedSocial(
                nombre=NombreRedSocial(red_dto.nombre),
                enlace=EnlaceRedSocial(red_dto.enlace),
                numero_seguidores=NumeroSeguidores(red_dto.numero_seguidores),
                engagement_rate=EngagementRate(red_dto.engagement_rate)
            )
            redes_sociales.append(red)

        influencer = InfluencerEntity(
            nombre=NombreInfluencer(influencer_dto.nombre),
            email=EmailInfluencer(influencer_dto.email),
            categoria=CategoriaInfluencer(influencer_dto.categoria),
            precio_por_post=PrecioPorPost(influencer_dto.precio_por_post),
            ubicacion=UbicacionInfluencer(influencer_dto.ubicacion),
            redes_sociales=redes_sociales
        )

        return influencer

    def _procesar_influencer_entidad(self, influencer: InfluencerEntity) -> InfluencerDTO:
        redes_dto = []
        for red in influencer.redes_sociales:
            red_dto = RedSocialDTO(
                nombre=red.nombre.valor,
                enlace=red.enlace.valor,
                numero_seguidores=red.numero_seguidores.valor,
                engagement_rate=red.engagement_rate.valor
            )
            redes_dto.append(red_dto)

        return InfluencerDTO(
            nombre=influencer.nombre.valor,
            email=influencer.email.valor,
            telefono="",  # Default value
            categoria=influencer.categoria.value,
            precio_por_post=influencer.precio_por_post.valor,
            redes_sociales=redes_dto,
            ubicacion=influencer.ubicacion.valor
        )

    def obtener_tipo(self) -> type:
        return Campana.__class__

    def entidad_a_dto(self, entidad: Campana) -> CampanaDTO:
        _id = str(entidad.id)
        fecha_creacion = str(entidad.fecha_creacion) if entidad.fecha_creacion else ''
        fecha_actualizacion = str(entidad.fecha_actualizacion) if entidad.fecha_actualizacion else ''
        
        influencers = []
        for inf in entidad.influencers:
            influencers.append(self._procesar_influencer_entidad(inf))

        hashtags = [hashtag.valor for hashtag in entidad.hashtags]

        return CampanaDTO(
            fecha_creacion=fecha_creacion, 
            fecha_actualizacion=fecha_actualizacion, 
            id=_id,
            nombre=entidad.nombre.valor,
            descripcion=entidad.descripcion.valor,
            fecha_inicio=entidad.fecha_inicio.valor.isoformat() if hasattr(entidad.fecha_inicio, 'valor') else '',
            fecha_fin=entidad.fecha_fin.valor.isoformat() if hasattr(entidad.fecha_fin, 'valor') else '',
            presupuesto=entidad.presupuesto.valor,
            objetivo=entidad.objetivo.value,
            audiencia_objetivo=entidad.audiencia_objetivo.valor,
            hashtags=hashtags,
            influencers=influencers
        )

    def dto_a_entidad(self, dto: CampanaDTO) -> Campana:
        fecha_inicio = None
        fecha_fin = None
        if dto.fecha_inicio:
            fecha_inicio = FechaInicio(datetime.fromisoformat(dto.fecha_inicio.replace('Z', '+00:00')))
        if dto.fecha_fin:
            fecha_fin = FechaFin(datetime.fromisoformat(dto.fecha_fin.replace('Z', '+00:00')))

        hashtags = [Hashtag(tag) for tag in dto.hashtags]
        influencers = []

        for inf_dto in dto.influencers:
            influencers.append(self._procesar_influencer_dto(inf_dto))

        campana = Campana(
            nombre=NombreCampana(dto.nombre),
            descripcion=DescripcionCampana(dto.descripcion),
            fecha_inicio=fecha_inicio if fecha_inicio else FechaInicio(),
            fecha_fin=fecha_fin if fecha_fin else FechaFin(),
            presupuesto=PresupuestoCampana(dto.presupuesto),
            objetivo=ObjetivoCampana(dto.objetivo),
            audiencia_objetivo=AudienciaObjetivo(dto.audiencia_objetivo),
            hashtags=hashtags,
            influencers=influencers
        )

        return campana
