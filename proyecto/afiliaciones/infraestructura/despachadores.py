import pulsar
from pulsar.schema import *
import os
import json
from datetime import datetime
from dominio.eventos import CampanaCreada, CampanaIniciada


class Despachador:
    def __init__(self):
        self.pulsar_url = os.getenv("PULSAR_URL", "pulsar://localhost:6650")
        self.cliente = pulsar.Client(self.pulsar_url)

    async def publicar_evento(self, evento, topico: str):
        try:
            # Crear esquema Avro para el evento
            if isinstance(evento, CampanaCreada):
                schema = self._crear_esquema_campana_creada()
                payload = self._crear_payload_campana_creada(evento)
            elif isinstance(evento, CampanaIniciada):
                schema = self._crear_esquema_campana_iniciada()
                payload = self._crear_payload_campana_iniciada(evento)
            else:
                raise ValueError(
                    f"Tipo de evento no soportado: {type(evento)}")

            # Crear productor
            productor = self.cliente.create_producer(topico, schema=schema)

            # Enviar mensaje
            productor.send(payload)
            print(f"Evento publicado en tópico {topico}: {evento}")

        except Exception as e:
            print(f"Error publicando evento: {e}")
        finally:
            if 'productor' in locals():
                productor.close()

    def _crear_esquema_campana_creada(self):
        return AvroSchema({
            "type": "record",
            "name": "CampanaCreadaEvent",
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "id_campana", "type": "string"},
                {"name": "id_marca", "type": "string"},
                {"name": "nombre", "type": "string"},
                {"name": "descripcion", "type": "string"},
                {"name": "tipo", "type": "string"},
                {"name": "estado", "type": "string"},
                {"name": "fecha_creacion", "type": "long"},
                {"name": "presupuesto", "type": "double"}
            ]
        })

    def _crear_esquema_campana_iniciada(self):
        return AvroSchema({
            "type": "record",
            "name": "CampanaIniciadaEvent",
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "id_campana", "type": "string"},
                {"name": "id_marca", "type": "string"},
                {"name": "estado", "type": "string"},
                {"name": "fecha_inicio", "type": "long"}
            ]
        })

    def _crear_payload_campana_creada(self, evento: CampanaCreada):
        return {
            "id": str(evento.id),
            "id_campana": str(evento.id_campana),
            "id_marca": str(evento.id_marca),
            "nombre": evento.nombre,
            "descripcion": evento.descripcion,
            "tipo": evento.tipo,
            "estado": evento.estado,
            "fecha_creacion": int(evento.fecha_creacion.timestamp() * 1000),
            "presupuesto": evento.presupuesto
        }

    def _crear_payload_campana_iniciada(self, evento: CampanaIniciada):
        return {
            "id": str(evento.id),
            "id_campana": str(evento.id_campana),
            "id_marca": str(evento.id_marca),
            "estado": evento.estado,
            "fecha_inicio": int(evento.fecha_inicio.timestamp() * 1000)
        }

    def cerrar(self):
        self.cliente.close()
