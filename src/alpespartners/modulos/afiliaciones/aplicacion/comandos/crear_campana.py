from alpespartners.seedwork.aplicacion.comandos import Comando
from alpespartners.modulos.afiliaciones.aplicacion.dto import InfluencerDTO, CampanaDTO
from dataclasses import dataclass
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando as comando

from alpespartners.modulos.afiliaciones.dominio.entidades import Campana
from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from alpespartners.modulos.afiliaciones.aplicacion.mapeadores import MapeadorCampana
from alpespartners.modulos.afiliaciones.infraestructura.repositorios import RepositorioCampanas
from alpespartners.modulos.afiliaciones.aplicacion.comandos.base import CampanaBaseHandler

@dataclass
class CrearCampana(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    influencers: list[InfluencerDTO]

class CrearCampanaHandler(CampanaBaseHandler):
    
    def handle(self, comando: CrearCampana):
        campana_dto = CampanaDTO(
            fecha_creacion=comando.fecha_creacion,
            fecha_actualizacion=comando.fecha_actualizacion, 
            id=comando.id,
            influencers=comando.influencers)

        campana: Campana = self.fabrica_afiliaciones.crear_objeto(campana_dto, MapeadorCampana())
        campana.crear_campana(campana)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampanas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, campana)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()
