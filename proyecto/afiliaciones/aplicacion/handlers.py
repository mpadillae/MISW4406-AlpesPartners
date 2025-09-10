from typing import List
import uuid
from .comandos.base import ManejadorComando
from .comandos.crear_campana import CrearCampana
from .comandos.iniciar_campana import IniciarCampana
from .queries.base import ManejadorQuery
from .queries.obtener_campana import ObtenerCampana, ObtenerTodasCampanas
from .dto import CampanaResponse, CampanaListResponse
from .mapeadores import MapeadorCampana
from .servicios import ServicioAplicacionCampana


class ManejadorCrearCampana(ManejadorComando):
    def __init__(self, servicio: ServicioAplicacionCampana):
        self.servicio = servicio

    async def ejecutar(self, comando: CrearCampana) -> CampanaResponse:
        campana = await self.servicio.crear_campana(
            id_marca=comando.id_marca,
            nombre=comando.nombre,
            descripcion=comando.descripcion,
            tipo=comando.tipo,
            presupuesto=comando.presupuesto
        )
        return MapeadorCampana.entidad_a_dto(campana)


class ManejadorIniciarCampana(ManejadorComando):
    def __init__(self, servicio: ServicioAplicacionCampana):
        self.servicio = servicio

    async def ejecutar(self, comando: IniciarCampana) -> CampanaResponse:
        campana = await self.servicio.iniciar_campana(comando.id_campana)
        return MapeadorCampana.entidad_a_dto(campana)


class ManejadorObtenerCampana(ManejadorQuery):
    def __init__(self, servicio: ServicioAplicacionCampana):
        self.servicio = servicio

    async def ejecutar(self, query: ObtenerCampana) -> CampanaResponse:
        campana = await self.servicio.obtener_campana(query.id_campana)
        return MapeadorCampana.entidad_a_dto(campana)


class ManejadorObtenerTodasCampanas(ManejadorQuery):
    def __init__(self, servicio: ServicioAplicacionCampana):
        self.servicio = servicio

    async def ejecutar(self, query: ObtenerTodasCampanas) -> CampanaListResponse:
        campanas = await self.servicio.obtener_todas_campanas()
        campanas_dto = [MapeadorCampana.entidad_a_dto(
            campana) for campana in campanas]
        return CampanaListResponse(campanas=campanas_dto, total=len(campanas_dto))
