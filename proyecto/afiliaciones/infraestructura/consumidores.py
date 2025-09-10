import pulsar
from pulsar.schema import *
import os
import json
import asyncio
from datetime import datetime


class ConsumidorEventos:
    def __init__(self):
        self.pulsar_url = os.getenv("PULSAR_URL", "pulsar://localhost:6650")
        self.cliente = pulsar.Client(self.pulsar_url)

    async def consumir_eventos(self, topico: str, suscripcion: str):
        try:
            # Crear esquema Avro
            schema = AvroSchema({
                "type": "record",
                "name": "EventoGenerico",
                "fields": [
                    {"name": "id", "type": "string"},
                    {"name": "tipo", "type": "string"},
                    {"name": "data", "type": "string"}
                ]
            })

            # Crear consumidor
            consumidor = self.cliente.subscribe(
                topico, suscripcion, schema=schema)

            print(f"Consumiendo eventos del tópico {topico}...")

            while True:
                try:
                    mensaje = consumidor.receive(timeout_millis=1000)
                    if mensaje:
                        evento_data = mensaje.value()
                        print(f"Evento recibido: {evento_data}")

                        # Procesar evento
                        await self._procesar_evento(evento_data)

                        # Confirmar mensaje
                        consumidor.acknowledge(mensaje)

                except pulsar.Timeout:
                    # Timeout normal, continuar
                    continue
                except Exception as e:
                    print(f"Error procesando mensaje: {e}")
                    consumidor.negative_acknowledge(mensaje)

        except Exception as e:
            print(f"Error en consumidor: {e}")
        finally:
            if 'consumidor' in locals():
                consumidor.close()

    async def _procesar_evento(self, evento_data):
        # Aquí se procesaría el evento específico
        # Por ahora solo imprimimos la información
        print(f"Procesando evento: {evento_data}")


async def iniciar_consumidores():
    consumidor = ConsumidorEventos()

    # Crear tareas para consumir diferentes tópicos
    tareas = [
        asyncio.create_task(consumidor.consumir_eventos(
            "eventos-campana", "afiliaciones-subscription")),
    ]

    # Ejecutar todas las tareas
    await asyncio.gather(*tareas)
