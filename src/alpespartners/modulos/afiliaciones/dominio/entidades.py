"""Entidades del dominio de afiliaciones

En este archivo usted encontrará las entidades del dominio de afiliaciones y marketing de influencers

"""

from __future__ import annotations
from dataclasses import dataclass, field
import uuid

import alpespartners.modulos.afiliaciones.dominio.objetos_valor as ov
from alpespartners.modulos.afiliaciones.dominio.eventos import CampanaCreada
from alpespartners.seedwork.dominio.entidades import Locacion, AgregacionRaiz, Entidad


@dataclass
class RedSocial(Entidad):
    nombre: ov.NombreRedSocial = field(default_factory=ov.NombreRedSocial)
    enlace: ov.EnlaceRedSocial = field(default_factory=ov.EnlaceRedSocial)
    numero_seguidores: ov.NumeroSeguidores = field(default_factory=ov.NumeroSeguidores)
    engagement_rate: ov.EngagementRate = field(default_factory=ov.EngagementRate)

    def __str__(self) -> str:
        return f"{self.nombre.valor} - {self.numero_seguidores.valor} seguidores"


@dataclass
class Influencer(Entidad):
    nombre: ov.NombreInfluencer = field(default_factory=ov.NombreInfluencer)
    email: ov.EmailInfluencer = field(default_factory=ov.EmailInfluencer)
    categoria: ov.CategoriaInfluencer = field(default_factory=ov.CategoriaInfluencer)
    precio_por_post: ov.PrecioPorPost = field(default_factory=ov.PrecioPorPost)
    ubicacion: ov.UbicacionInfluencer = field(default_factory=ov.UbicacionInfluencer)
    redes_sociales: list[ov.RedSocial] = field(default_factory=list[ov.RedSocial])

    def calcular_alcance_total(self):
        return sum(red.numero_seguidores.valor for red in self.redes_sociales)


@dataclass
class Metrica(Entidad):
    nombre: ov.NombreMetrica = field(default_factory=ov.NombreMetrica)
    valor: ov.ValorMetrica = field(default_factory=ov.ValorMetrica)
    fecha_medicion: ov.FechaMedicion = field(default_factory=ov.FechaMedicion)


@dataclass
class Contenido(Entidad):
    tipo: ov.TipoContenido = field(default_factory=ov.TipoContenido)
    descripcion: ov.DescripcionContenido = field(default_factory=ov.DescripcionContenido)
    url_contenido: ov.UrlContenido = field(default_factory=ov.UrlContenido)
    fecha_publicacion: ov.FechaPublicacion = field(default_factory=ov.FechaPublicacion)
    influencer: Influencer = field(default_factory=Influencer)
    metricas: list[ov.Metrica] = field(default_factory=list[ov.Metrica])


@dataclass
class Campana(AgregacionRaiz):
    id_marca: uuid.UUID = field(hash=True, default=None)
    nombre: ov.NombreCampana = field(default_factory=ov.NombreCampana)
    descripcion: ov.DescripcionCampana = field(default_factory=ov.DescripcionCampana)
    fecha_inicio: ov.FechaInicio = field(default_factory=ov.FechaInicio)
    fecha_fin: ov.FechaFin = field(default_factory=ov.FechaFin)
    presupuesto: ov.PresupuestoCampana = field(default_factory=ov.PresupuestoCampana)
    objetivo: ov.ObjetivoCampana = field(default_factory=ov.ObjetivoCampana)
    audiencia_objetivo: ov.AudienciaObjetivo = field(default_factory=ov.AudienciaObjetivo)
    estado: ov.EstadoCampana = field(default=ov.EstadoCampana.PENDIENTE)
    hashtags: list[ov.Hashtag] = field(default_factory=list[ov.Hashtag])
    influencers: list[ov.Influencer] = field(default_factory=list[ov.Influencer])
    contenidos: list[ov.Contenido] = field(default_factory=list[ov.Contenido])

    def crear_campana(self, campana: Campana):
        self.id_marca = campana.id_marca
        self.nombre = campana.nombre
        self.descripcion = campana.descripcion
        self.fecha_inicio = campana.fecha_inicio
        self.fecha_fin = campana.fecha_fin
        self.presupuesto = campana.presupuesto
        self.objetivo = campana.objetivo
        self.audiencia_objetivo = campana.audiencia_objetivo
        self.estado = campana.estado
        self.hashtags = campana.hashtags
        self.influencers = campana.influencers
        self.contenidos = campana.contenidos

        self.agregar_evento(CampanaCreada(id_campana=self.id, id_marca=self.id_marca,
                            estado=self.estado.name, fecha_creacion=self.fecha_creacion))
