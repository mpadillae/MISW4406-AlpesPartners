from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import uuid
from pydantic import BaseModel
from dominio.servicios import ServicioTracking
from infraestructura.repositorios import RepositorioMetricasCampanaSQLAlchemy, RepositorioEventoTrackingSQLAlchemy

router = APIRouter()

# DTOs


class EventoTrackingRequest(BaseModel):
    id_campana: uuid.UUID
    tipo_evento: str
    datos: Dict[str, Any]


class MetricasResponse(BaseModel):
    id: uuid.UUID
    id_campana: uuid.UUID
    id_marca: uuid.UUID
    nombre_campana: str
    estado: str
    fecha_creacion: str
    fecha_inicio: str = None
    presupuesto: float
    metricas: Dict[str, Any]


class EventoTrackingResponse(BaseModel):
    id: uuid.UUID
    id_campana: uuid.UUID
    tipo_evento: str
    datos: Dict[str, Any]
    fecha_evento: str

# Dependencias


def obtener_servicio_tracking() -> ServicioTracking:
    repositorio_metricas = RepositorioMetricasCampanaSQLAlchemy()
    repositorio_eventos = RepositorioEventoTrackingSQLAlchemy()
    return ServicioTracking(repositorio_metricas, repositorio_eventos)


@router.post("/evento")
async def registrar_evento_tracking(
    request: EventoTrackingRequest,
    servicio: ServicioTracking = Depends(obtener_servicio_tracking)
):
    try:
        evento = servicio.registrar_evento_tracking(
            id_campana=request.id_campana,
            tipo_evento=request.tipo_evento,
            datos=request.datos
        )

        return EventoTrackingResponse(
            id=evento.id,
            id_campana=evento.id_campana,
            tipo_evento=evento.tipo_evento,
            datos=evento.datos,
            fecha_evento=evento.fecha_evento.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metricas/{id_campana}")
async def obtener_metricas_campana(
    id_campana: uuid.UUID,
    servicio: ServicioTracking = Depends(obtener_servicio_tracking)
):
    try:
        metricas = servicio.obtener_metricas_campana(id_campana)
        if not metricas:
            raise HTTPException(
                status_code=404, detail="Métricas no encontradas")

        return MetricasResponse(
            id=metricas.id,
            id_campana=metricas.id_campana,
            id_marca=metricas.id_marca,
            nombre_campana=metricas.nombre_campana,
            estado=metricas.estado,
            fecha_creacion=metricas.fecha_creacion.isoformat(),
            fecha_inicio=metricas.fecha_inicio.isoformat() if metricas.fecha_inicio else None,
            presupuesto=metricas.presupuesto,
            metricas=metricas.metricas
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/eventos/{id_campana}")
async def obtener_eventos_campana(
    id_campana: uuid.UUID,
    servicio: ServicioTracking = Depends(obtener_servicio_tracking)
):
    try:
        eventos = servicio.obtener_eventos_campana(id_campana)

        return [
            EventoTrackingResponse(
                id=evento.id,
                id_campana=evento.id_campana,
                tipo_evento=evento.tipo_evento,
                datos=evento.datos,
                fecha_evento=evento.fecha_evento.isoformat()
            )
            for evento in eventos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metricas/marca/{id_marca}")
async def obtener_metricas_por_marca(
    id_marca: uuid.UUID,
    servicio: ServicioTracking = Depends(obtener_servicio_tracking)
):
    try:
        metricas_list = servicio.obtener_metricas_por_marca(id_marca)

        return [
            MetricasResponse(
                id=metricas.id,
                id_campana=metricas.id_campana,
                id_marca=metricas.id_marca,
                nombre_campana=metricas.nombre_campana,
                estado=metricas.estado,
                fecha_creacion=metricas.fecha_creacion.isoformat(),
                fecha_inicio=metricas.fecha_inicio.isoformat() if metricas.fecha_inicio else None,
                presupuesto=metricas.presupuesto,
                metricas=metricas.metricas
            )
            for metricas in metricas_list
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
