import pulsar
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
            # Crear payload JSON para el evento
            if isinstance(evento, CampanaCreada):
                payload = self._crear_payload_campana_creada(evento)
            elif isinstance(evento, CampanaIniciada):
                payload = self._crear_payload_campana_iniciada(evento)
            else:
                raise ValueError(
                    f"Tipo de evento no soportado: {type(evento)}")

            # Crear productor (sin schema para usar JSON)
            productor = self.cliente.create_producer(topico)

            # Enviar mensaje como JSON
            mensaje_json = json.dumps(payload)
            productor.send(mensaje_json.encode('utf-8'))
            print(f"Evento publicado en tópico {topico}: {evento}")

        except Exception as e:
            print(f"Error publicando evento: {e}")

        finally:
            if 'productor' in locals():
                productor.close()

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
