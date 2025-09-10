from sqlalchemy import create_engine, Column, String, DateTime, Float, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
import uuid
import os
from datetime import datetime

from dominio.entidades import Campana
from dominio.repositorios import RepositorioCampana
from .dto import CampanaDTO

Base = declarative_base()


class CampanaDB(Base):
    __tablename__ = "campanas"

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_marca = Column(UUID(as_uuid=True), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=False)
    tipo = Column(String(20), nullable=False)
    estado = Column(String(20), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    presupuesto = Column(Float, nullable=False)


class RepositorioCampanaSQLAlchemy(RepositorioCampana):
    def __init__(self):
        database_url = os.getenv(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/afiliaciones")
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        self.session = SessionLocal()

    def obtener_por_id(self, id_campana: uuid.UUID) -> Optional[Campana]:
        campana_db = self.session.query(CampanaDB).filter(
            CampanaDB.id == id_campana).first()
        if campana_db:
            return self._db_a_entidad(campana_db)
        return None

    def obtener_todas(self) -> List[Campana]:
        campanas_db = self.session.query(CampanaDB).all()
        return [self._db_a_entidad(campana_db) for campana_db in campanas_db]

    def agregar(self, campana: Campana) -> Campana:
        campana_db = self._entidad_a_db(campana)
        self.session.add(campana_db)
        self.session.commit()
        self.session.refresh(campana_db)
        return self._db_a_entidad(campana_db)

    def actualizar(self, campana: Campana) -> Campana:
        campana_db = self.session.query(CampanaDB).filter(
            CampanaDB.id == campana.id).first()
        if campana_db:
            campana_db.nombre = campana.nombre
            campana_db.descripcion = campana.descripcion
            campana_db.tipo = campana.tipo.value if campana.tipo else "influencer"
            campana_db.estado = campana.estado.value if campana.estado else "creada"
            campana_db.fecha_inicio = campana.fecha_inicio
            campana_db.fecha_fin = campana.fecha_fin
            campana_db.presupuesto = campana.presupuesto
            self.session.commit()
            return self._db_a_entidad(campana_db)
        return campana

    def eliminar(self, id_campana: uuid.UUID) -> bool:
        campana_db = self.session.query(CampanaDB).filter(
            CampanaDB.id == id_campana).first()
        if campana_db:
            self.session.delete(campana_db)
            self.session.commit()
            return True
        return False

    def _entidad_a_db(self, campana: Campana) -> CampanaDB:
        return CampanaDB(
            id=campana.id,
            id_marca=campana.id_marca,
            nombre=campana.nombre,
            descripcion=campana.descripcion,
            tipo=campana.tipo.value if campana.tipo else "influencer",
            estado=campana.estado.value if campana.estado else "creada",
            fecha_creacion=campana.fecha_creacion,
            fecha_inicio=campana.fecha_inicio,
            fecha_fin=campana.fecha_fin,
            presupuesto=campana.presupuesto
        )

    def _db_a_entidad(self, campana_db: CampanaDB) -> Campana:
        from dominio.objetos_valor import TipoCampana, EstadoCampana

        return Campana(
            id=campana_db.id,
            id_marca=campana_db.id_marca,
            nombre=campana_db.nombre,
            descripcion=campana_db.descripcion,
            tipo=TipoCampana(campana_db.tipo),
            estado=EstadoCampana(campana_db.estado),
            fecha_creacion=campana_db.fecha_creacion,
            fecha_inicio=campana_db.fecha_inicio,
            fecha_fin=campana_db.fecha_fin,
            presupuesto=campana_db.presupuesto
        )
