from sqlalchemy import create_engine, Column, String, DateTime, Float, UUID, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
import uuid
import os
from datetime import datetime

from dominio.entidades import Marca, CampanaMarca
from dominio.repositorios import RepositorioMarca, RepositorioCampanaMarca

Base = declarative_base()


class MarcaDB(Base):
    __tablename__ = "marcas"

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_marca = Column(UUID(as_uuid=True), nullable=False)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    activa = Column(Boolean, default=True)


class CampanaMarcaDB(Base):
    __tablename__ = "campanas_marca"

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_campana = Column(UUID(as_uuid=True), nullable=False)
    id_marca = Column(UUID(as_uuid=True), nullable=False)
    nombre_campana = Column(String(100), nullable=False)
    estado = Column(String(20), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_inicio = Column(DateTime, nullable=True)
    presupuesto = Column(Float, nullable=False)


class RepositorioMarcaSQLAlchemy(RepositorioMarca):
    def __init__(self):
        database_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/marca")
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()

    def obtener_por_id(self, id_marca: uuid.UUID) -> Optional[Marca]:
        marca_db = self.session.query(MarcaDB).filter(
            MarcaDB.id_marca == id_marca).first()
        if marca_db:
            return self._db_a_entidad(marca_db)
        return None

    def obtener_todas(self) -> List[Marca]:
        marcas_db = self.session.query(MarcaDB).all()
        return [self._db_a_entidad(marca_db) for marca_db in marcas_db]

    def agregar(self, marca: Marca) -> Marca:
        marca_db = self._entidad_a_db(marca)
        self.session.add(marca_db)
        self.session.commit()
        self.session.refresh(marca_db)
        return self._db_a_entidad(marca_db)

    def actualizar(self, marca: Marca) -> Marca:
        marca_db = self.session.query(MarcaDB).filter(
            MarcaDB.id == marca.id).first()
        if marca_db:
            marca_db.nombre = marca.nombre
            marca_db.categoria = marca.categoria
            marca_db.activa = marca.activa
            self.session.commit()
            return self._db_a_entidad(marca_db)
        return marca

    def _entidad_a_db(self, marca: Marca) -> MarcaDB:
        return MarcaDB(
            id=marca.id,
            id_marca=marca.id_marca,
            nombre=marca.nombre,
            categoria=marca.categoria,
            fecha_creacion=marca.fecha_creacion,
            activa=marca.activa
        )

    def _db_a_entidad(self, marca_db: MarcaDB) -> Marca:
        return Marca(
            id=marca_db.id,
            id_marca=marca_db.id_marca,
            nombre=marca_db.nombre,
            categoria=marca_db.categoria,
            fecha_creacion=marca_db.fecha_creacion,
            activa=marca_db.activa
        )


class RepositorioCampanaMarcaSQLAlchemy(RepositorioCampanaMarca):
    def __init__(self):
        database_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/marca")
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()

    def obtener_por_id(self, id_campana: uuid.UUID) -> Optional[CampanaMarca]:
        campana_db = self.session.query(CampanaMarcaDB).filter(
            CampanaMarcaDB.id_campana == id_campana).first()
        if campana_db:
            return self._db_a_entidad(campana_db)
        return None

    def obtener_por_marca(self, id_marca: uuid.UUID) -> List[CampanaMarca]:
        campanas_db = self.session.query(CampanaMarcaDB).filter(
            CampanaMarcaDB.id_marca == id_marca).all()
        return [self._db_a_entidad(campana_db) for campana_db in campanas_db]

    def obtener_todas(self) -> List[CampanaMarca]:
        campanas_db = self.session.query(CampanaMarcaDB).all()
        return [self._db_a_entidad(campana_db) for campana_db in campanas_db]

    def agregar(self, campana: CampanaMarca) -> CampanaMarca:
        campana_db = self._entidad_a_db(campana)
        self.session.add(campana_db)
        self.session.commit()
        self.session.refresh(campana_db)
        return self._db_a_entidad(campana_db)

    def actualizar(self, campana: CampanaMarca) -> CampanaMarca:
        campana_db = self.session.query(CampanaMarcaDB).filter(
            CampanaMarcaDB.id == campana.id).first()
        if campana_db:
            campana_db.estado = campana.estado
            campana_db.fecha_inicio = campana.fecha_inicio
            self.session.commit()
            return self._db_a_entidad(campana_db)
        return campana

    def _entidad_a_db(self, campana: CampanaMarca) -> CampanaMarcaDB:
        return CampanaMarcaDB(
            id=campana.id,
            id_campana=campana.id_campana,
            id_marca=campana.id_marca,
            nombre_campana=campana.nombre_campana,
            estado=campana.estado,
            fecha_creacion=campana.fecha_creacion,
            fecha_inicio=campana.fecha_inicio,
            presupuesto=campana.presupuesto
        )

    def _db_a_entidad(self, campana_db: CampanaMarcaDB) -> CampanaMarca:
        return CampanaMarca(
            id=campana_db.id,
            id_campana=campana_db.id_campana,
            id_marca=campana_db.id_marca,
            nombre_campana=campana_db.nombre_campana,
            estado=campana_db.estado,
            fecha_creacion=campana_db.fecha_creacion,
            fecha_inicio=campana_db.fecha_inicio,
            presupuesto=campana_db.presupuesto
        )
