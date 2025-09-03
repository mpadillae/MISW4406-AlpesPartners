""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de afiliaciones

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de afiliaciones

"""

from alpespartners.config.db import db
from alpespartners.modulos.afiliaciones.dominio.repositorios import RepositorioCampanas, RepositorioInfluencers
from alpespartners.modulos.afiliaciones.dominio.objetos_valor import *
from alpespartners.modulos.afiliaciones.dominio.entidades import Campana, Influencer, RedSocial
from alpespartners.modulos.afiliaciones.dominio.fabricas import FabricaAfiliaciones
from .dto import Campana as CampanaDTO
from .mapeadores import MapeadorCampana
from uuid import UUID

class RepositorioInfluencersSQLite(RepositorioInfluencers):

    def obtener_por_id(self, id: UUID) -> Influencer:
        raise NotImplementedError

    def obtener_todos(self) -> list[Influencer]:
        # Ejemplo de influencer de muestra
        red_social = RedSocial(
            nombre=NombreRedSocial("Instagram"),
            enlace=EnlaceRedSocial("https://instagram.com/influencer1"),
            numero_seguidores=NumeroSeguidores(50000),
            engagement_rate=EngagementRate(3.5)
        )
        
        influencer = Influencer(
            nombre=NombreInfluencer("Ana García"),
            email=EmailInfluencer("ana@email.com"),
            categoria=CategoriaInfluencer.MODA,
            precio_por_post=PrecioPorPost(500.0),
            ubicacion=UbicacionInfluencer("Madrid, España"),
            redes_sociales=[red_social]
        )
        return [influencer]

    def agregar(self, entity: Influencer):
        raise NotImplementedError

    def actualizar(self, entity: Influencer):
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        raise NotImplementedError


class RepositorioCampanasSQLite(RepositorioCampanas):

    def __init__(self):
        self._fabrica_afiliaciones: FabricaAfiliaciones = FabricaAfiliaciones()

    @property
    def fabrica_afiliaciones(self):
        return self._fabrica_afiliaciones

    def obtener_por_id(self, id: UUID) -> Campana:
        campana_dto = db.session.query(CampanaDTO).filter_by(id=str(id)).one()
        return self.fabrica_afiliaciones.crear_objeto(campana_dto, MapeadorCampana())

    def obtener_todos(self) -> list[Campana]:
        raise NotImplementedError

    def agregar(self, campana: Campana):
        campana_dto = self.fabrica_afiliaciones.crear_objeto(campana, MapeadorCampana())
        db.session.add(campana_dto)

    def actualizar(self, campana: Campana):
        raise NotImplementedError

    def eliminar(self, campana_id: UUID):
        raise NotImplementedError