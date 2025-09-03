from alpespartners.seedwork.aplicacion.servicios import Servicio
from alpespartners.modulos.afiliaciones.dominio.entidades import Campana
from alpespartners.modulos.afiliaciones.dominio.fabricas import FabricaAfiliaciones
from alpespartners.modulos.afiliaciones.infraestructura.fabricas import FabricaRepositorio
from alpespartners.modulos.afiliaciones.infraestructura.repositorios import RepositorioCampanas
from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorCampana

from .dto import CampanaDTO

import asyncio

class ServicioCampana(Servicio):

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_afiliaciones: FabricaAfiliaciones = FabricaAfiliaciones()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_afiliaciones(self):
        return self._fabrica_afiliaciones       
    
    def crear_campana(self, campana_dto: CampanaDTO) -> CampanaDTO:
        campana: Campana = self.fabrica_afiliaciones.crear_objeto(campana_dto, MapeadorCampana())
        campana.crear_campana(campana)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampanas.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, campana)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return self.fabrica_afiliaciones.crear_objeto(campana, MapeadorCampana())

    def obtener_campana_por_id(self, id) -> CampanaDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioCampanas.__class__)
        return self.fabrica_afiliaciones.crear_objeto(repositorio.obtener_por_id(id), MapeadorCampana())

