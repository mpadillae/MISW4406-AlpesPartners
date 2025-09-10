from sqlalchemy import create_engine, Column, String, DateTime, Float, UUID, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional, Dict, Any
import uuid
import os
from datetime import datetime

from dominio.entidades import MetricasCampana, EventoTracking
from dominio.repositorios import RepositorioMetricasCampana, RepositorioEventoTracking

Base = declarative_base()


class MetricasCampanaDB(Base):
    __tablename__ = "metricas_campana"

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_campana = Column(UUID(as_uuid=True), nullable=False)
    id_marca = Column(UUID(as_uuid=True), nullable=False)
    nombre_campana = Column(String(100), nullable=False)
    estado = Column(String(20), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_inicio = Column(DateTime, nullable=True)
    presupuesto = Column(Float, nullable=False)
    metricas = Column(JSON, nullable=False)


class EventoTrackingDB(Base):
    __tablename__ = "eventos_tracking"

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_campana = Column(UUID(as_uuid=True), nullable=False)
    tipo_evento = Column(String(50), nullable=True)
    datos = Column(JSON, nullable=False)
    fecha_evento = Column(DateTime, nullable=False)


class RepositorioMetricasCampanaSQLAlchemy(RepositorioMetricasCampana):
    def __init__(self):
        database_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tracking")
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()

    def obtener_por_id(self, id_campana: uuid.UUID) -> Optional[MetricasCampana]:
        metricas_db = self.session.query(MetricasCampanaDB).filter(
            MetricasCampanaDB.id_campana == id_campana).first()
        if metricas_db:
            return self._db_a_entidad(metricas_db)
        return None

    def obtener_por_marca(self, id_marca: uuid.UUID) -> List[MetricasCampana]:
        metricas_db = self.session.query(MetricasCampanaDB).filter(
            MetricasCampanaDB.id_marca == id_marca).all()
        return [self._db_a_entidad(metricas_db) for metricas_db in metricas_db]

    def obtener_todas(self) -> List[MetricasCampana]:
        metricas_db = self.session.query(MetricasCampanaDB).all()
        return [self._db_a_entidad(metricas_db) for metricas_db in metricas_db]

    def agregar(self, metricas: MetricasCampana) -> MetricasCampana:
        metricas_db = self._entidad_a_db(metricas)
        self.session.add(metricas_db)
        self.session.commit()
        self.session.refresh(metricas_db)
        return self._db_a_entidad(metricas_db)

    def actualizar(self, metricas: MetricasCampana) -> MetricasCampana:
        metricas_db = self.session.query(MetricasCampanaDB).filter(
            MetricasCampanaDB.id == metricas.id).first()
        if metricas_db:
            metricas_db.estado = metricas.estado
            metricas_db.fecha_inicio = metricas.fecha_inicio
            metricas_db.metricas = metricas.metricas
            self.session.commit()
            return self._db_a_entidad(metricas_db)
        return metricas

    def _entidad_a_db(self, metricas: MetricasCampana) -> MetricasCampanaDB:
        return MetricasCampanaDB(
            id=metricas.id,
            id_campana=metricas.id_campana,
            id_marca=metricas.id_marca,
            nombre_campana=metricas.nombre_campana,
            estado=metricas.estado,
            fecha_creacion=metricas.fecha_creacion,
            fecha_inicio=metricas.fecha_inicio,
            presupuesto=metricas.presupuesto,
            metricas=metricas.metricas
        )

    def _db_a_entidad(self, metricas_db: MetricasCampanaDB) -> MetricasCampana:
        return MetricasCampana(
            id=metricas_db.id,
            id_campana=metricas_db.id_campana,
            id_marca=metricas_db.id_marca,
            nombre_campana=metricas_db.nombre_campana,
            estado=metricas_db.estado,
            fecha_creacion=metricas_db.fecha_creacion,
            fecha_inicio=metricas_db.fecha_inicio,
            presupuesto=metricas_db.presupuesto,
            metricas=metricas_db.metricas
        )


class RepositorioEventoTrackingSQLAlchemy(RepositorioEventoTracking):
    def __init__(self):
        database_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tracking")
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()

    def obtener_por_campana(self, id_campana: uuid.UUID) -> List[EventoTracking]:
        eventos_db = self.session.query(EventoTrackingDB).filter(
            EventoTrackingDB.id_campana == id_campana).all()
        return [self._db_a_entidad(evento_db) for evento_db in eventos_db]

    def obtener_por_tipo(self, tipo_evento: str) -> List[EventoTracking]:
        eventos_db = self.session.query(EventoTrackingDB).filter(
            EventoTrackingDB.tipo_evento == tipo_evento).all()
        return [self._db_a_entidad(evento_db) for evento_db in eventos_db]

    def obtener_todos(self) -> List[EventoTracking]:
        eventos_db = self.session.query(EventoTrackingDB).all()
        return [self._db_a_entidad(evento_db) for evento_db in eventos_db]

    def agregar(self, evento: EventoTracking) -> EventoTracking:
        evento_db = self._entidad_a_db(evento)
        self.session.add(evento_db)
        self.session.commit()
        self.session.refresh(evento_db)
        return self._db_a_entidad(evento_db)

    def _entidad_a_db(self, evento: EventoTracking) -> EventoTrackingDB:
        print(f"[RepositorioEventoTrackingSQLAlchemy] Entidad a DB: {evento}")
        return EventoTrackingDB(
            id=evento.id,
            id_campana=evento.id_campana,
            tipo_evento=evento.tipo_evento,
            datos=evento.datos,
            fecha_evento=evento.fecha_evento
        )

    def _db_a_entidad(self, evento_db: EventoTrackingDB) -> EventoTracking:
        return EventoTracking(
            id=evento_db.id,
            id_campana=evento_db.id_campana,
            tipo_evento=evento_db.tipo_evento,
            datos=evento_db.datos,
            fecha_evento=evento_db.fecha_evento
        )
