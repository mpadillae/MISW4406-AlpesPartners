from sqlalchemy import create_engine, Column, String, DateTime, Float, UUID, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
import uuid
import os
from datetime import datetime

from dominio.entidades import Influencer, CampanaInfluencer
from dominio.repositorios import RepositorioInfluencer, RepositorioCampanaInfluencer

Base = declarative_base()


class InfluencerDB(Base):
    __tablename__ = "influencers"

    id = Column(UUID(as_uuid=True), primary_key=True)
    nombre = Column(String(100), nullable=False)
    plataforma = Column(String(50), nullable=False)
    seguidores = Column(Integer, default=0)
    categoria = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, nullable=False)


class CampanaInfluencerDB(Base):
    __tablename__ = "campanas_influencer"

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_campana = Column(UUID(as_uuid=True), nullable=False)
    id_influencer = Column(UUID(as_uuid=True), nullable=True)
    id_marca = Column(UUID(as_uuid=True), nullable=False)
    nombre_campana = Column(String(100), nullable=False)
    estado = Column(String(20), nullable=False)
    fecha_asignacion = Column(DateTime, nullable=False)
    fecha_inicio = Column(DateTime, nullable=True)
    presupuesto_asignado = Column(Float, nullable=False)


class RepositorioInfluencerSQLAlchemy(RepositorioInfluencer):
    def __init__(self):
        database_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/influencer")
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()

    def obtener_por_id(self, id_influencer: uuid.UUID) -> Optional[Influencer]:
        influencer_db = self.session.query(InfluencerDB).filter(
            InfluencerDB.id == id_influencer).first()
        if influencer_db:
            return self._db_a_entidad(influencer_db)
        return None

    def obtener_por_categoria(self, categoria: str) -> List[Influencer]:
        influencers_db = self.session.query(InfluencerDB).filter(
            InfluencerDB.categoria == categoria).all()
        return [self._db_a_entidad(influencer_db) for influencer_db in influencers_db]

    def obtener_todos(self) -> List[Influencer]:
        influencers_db = self.session.query(InfluencerDB).all()
        return [self._db_a_entidad(influencer_db) for influencer_db in influencers_db]

    def agregar(self, influencer: Influencer) -> Influencer:
        influencer_db = self._entidad_a_db(influencer)
        self.session.add(influencer_db)
        self.session.commit()
        self.session.refresh(influencer_db)
        return self._db_a_entidad(influencer_db)

    def actualizar(self, influencer: Influencer) -> Influencer:
        influencer_db = self.session.query(InfluencerDB).filter(
            InfluencerDB.id == influencer.id).first()
        if influencer_db:
            influencer_db.nombre = influencer.nombre
            influencer_db.plataforma = influencer.plataforma
            influencer_db.seguidores = influencer.seguidores
            influencer_db.categoria = influencer.categoria
            influencer_db.activo = influencer.activo
            self.session.commit()
            return self._db_a_entidad(influencer_db)
        return influencer

    def _entidad_a_db(self, influencer: Influencer) -> InfluencerDB:
        return InfluencerDB(
            id=influencer.id,
            nombre=influencer.nombre,
            plataforma=influencer.plataforma,
            seguidores=influencer.seguidores,
            categoria=influencer.categoria,
            activo=influencer.activo,
            fecha_registro=influencer.fecha_registro
        )

    def _db_a_entidad(self, influencer_db: InfluencerDB) -> Influencer:
        return Influencer(
            id=influencer_db.id,
            nombre=influencer_db.nombre,
            plataforma=influencer_db.plataforma,
            seguidores=influencer_db.seguidores,
            categoria=influencer_db.categoria,
            activo=influencer_db.activo,
            fecha_registro=influencer_db.fecha_registro
        )


class RepositorioCampanaInfluencerSQLAlchemy(RepositorioCampanaInfluencer):
    def __init__(self):
        database_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/influencer")
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()

    def obtener_por_id(self, id_campana: uuid.UUID) -> Optional[CampanaInfluencer]:
        campana_db = self.session.query(CampanaInfluencerDB).filter(
            CampanaInfluencerDB.id_campana == id_campana).first()
        if campana_db:
            return self._db_a_entidad(campana_db)
        return None

    def obtener_por_influencer(self, id_influencer: uuid.UUID) -> List[CampanaInfluencer]:
        campanas_db = self.session.query(CampanaInfluencerDB).filter(
            CampanaInfluencerDB.id_influencer == id_influencer).all()
        return [self._db_a_entidad(campana_db) for campana_db in campanas_db]

    def obtener_todas(self) -> List[CampanaInfluencer]:
        campanas_db = self.session.query(CampanaInfluencerDB).all()
        return [self._db_a_entidad(campana_db) for campana_db in campanas_db]

    def agregar(self, campana: CampanaInfluencer) -> CampanaInfluencer:
        campana_db = self._entidad_a_db(campana)
        self.session.add(campana_db)
        self.session.commit()
        self.session.refresh(campana_db)
        return self._db_a_entidad(campana_db)

    def actualizar(self, campana: CampanaInfluencer) -> CampanaInfluencer:
        campana_db = self.session.query(CampanaInfluencerDB).filter(
            CampanaInfluencerDB.id == campana.id).first()
        if campana_db:
            campana_db.estado = campana.estado
            campana_db.fecha_inicio = campana.fecha_inicio
            campana_db.id_influencer = campana.id_influencer
            self.session.commit()
            return self._db_a_entidad(campana_db)
        return campana

    def _entidad_a_db(self, campana: CampanaInfluencer) -> CampanaInfluencerDB:
        return CampanaInfluencerDB(
            id=campana.id,
            id_campana=campana.id_campana,
            id_influencer=campana.id_influencer,
            id_marca=campana.id_marca,
            nombre_campana=campana.nombre_campana,
            estado=campana.estado,
            fecha_asignacion=campana.fecha_asignacion,
            fecha_inicio=campana.fecha_inicio,
            presupuesto_asignado=campana.presupuesto_asignado
        )

    def _db_a_entidad(self, campana_db: CampanaInfluencerDB) -> CampanaInfluencer:
        return CampanaInfluencer(
            id=campana_db.id,
            id_campana=campana_db.id_campana,
            id_influencer=campana_db.id_influencer,
            id_marca=campana_db.id_marca,
            nombre_campana=campana_db.nombre_campana,
            estado=campana_db.estado,
            fecha_asignacion=campana_db.fecha_asignacion,
            fecha_inicio=campana_db.fecha_inicio,
            presupuesto_asignado=campana_db.presupuesto_asignado
        )
