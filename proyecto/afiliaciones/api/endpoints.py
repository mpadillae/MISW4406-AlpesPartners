from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from aplicacion.dto import CrearCampanaRequest, CampanaResponse, IniciarCampanaRequest, CampanaListResponse
from aplicacion.comandos.crear_campana import CrearCampana
from aplicacion.comandos.iniciar_campana import IniciarCampana
from aplicacion.queries.obtener_campana import ObtenerCampana, ObtenerTodasCampanas
from aplicacion.handlers import (
    ManejadorCrearCampana,
    ManejadorIniciarCampana,
    ManejadorObtenerCampana,
    ManejadorObtenerTodasCampanas
)
from aplicacion.servicios import ServicioAplicacionCampana
from infraestructura.fabricas import FabricaRepositorio, FabricaDespachador

router = APIRouter()

# Dependencias


def obtener_servicio_campana() -> ServicioAplicacionCampana:
    repositorio = FabricaRepositorio.crear_repositorio_campana()
    despachador = FabricaDespachador.crear_despachador()
    return ServicioAplicacionCampana(repositorio, despachador)


@router.post("/campana", response_model=CampanaResponse)
async def crear_campana(
    request: CrearCampanaRequest,
    servicio: ServicioAplicacionCampana = Depends(obtener_servicio_campana)
):
    try:
        comando = CrearCampana(
            id_marca=request.id_marca,
            nombre=request.nombre,
            descripcion=request.descripcion,
            tipo=request.tipo,
            presupuesto=request.presupuesto
        )

        manejador = ManejadorCrearCampana(servicio)
        resultado = await manejador.ejecutar(comando)

        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/campana/{id_campana}/iniciar", response_model=CampanaResponse)
async def iniciar_campana(
    id_campana: uuid.UUID,
    servicio: ServicioAplicacionCampana = Depends(obtener_servicio_campana)
):
    try:
        comando = IniciarCampana(id_campana=id_campana)
        manejador = ManejadorIniciarCampana(servicio)
        resultado = await manejador.ejecutar(comando)

        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/campana/{id_campana}", response_model=CampanaResponse)
async def obtener_campana(
    id_campana: uuid.UUID,
    servicio: ServicioAplicacionCampana = Depends(obtener_servicio_campana)
):
    try:
        query = ObtenerCampana(id_campana=id_campana)
        manejador = ManejadorObtenerCampana(servicio)
        resultado = await manejador.ejecutar(query)

        return resultado
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/campanas", response_model=CampanaListResponse)
async def obtener_todas_campanas(
    servicio: ServicioAplicacionCampana = Depends(obtener_servicio_campana)
):
    try:
        query = ObtenerTodasCampanas()
        manejador = ManejadorObtenerTodasCampanas(servicio)
        resultado = await manejador.ejecutar(query)

        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
