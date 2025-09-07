"""DTOs para la capa de infrastructura del dominio de afiliaciones

En este archivo usted encontrará los DTOs para el
la infraestructura del dominio de afiliaciones

"""

from alpespartners.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla campanas e influencers
campanas_influencers = db.Table(
    "campanas_influencers",
    db.Model.metadata,
    db.Column("campana_id", db.String, db.ForeignKey("campanas.id")),
    db.Column("influencer_id", db.String, db.ForeignKey("influencers.id")),
)

class Influencer(db.Model):
    __tablename__ = "influencers"
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    red_social = db.Column(db.String, nullable=False)
    seguidores = db.Column(db.Integer, nullable=False)
    costo_por_post = db.Column(db.Float, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)


class Campana(db.Model):
    __tablename__ = "campanas"
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    objetivo = db.Column(db.String, nullable=False)
    audiencia_objetivo = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    presupuesto = db.Column(db.Float, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    influencers = db.relationship('Influencer', secondary=campanas_influencers, backref='campanas')
