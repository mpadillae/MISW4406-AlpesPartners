import pulsar
from pulsar.schema import *
import os
import json
import asyncio
from datetime import datetime
from dominio.servicios import ServicioMarca
from .repositorios import RepositorioMarcaSQLAlchemy, RepositorioCampanaMarcaSQLAlchemy


class ConsumidorEventosMarca:
    def __init__(self):
        self.pulsar_url = os.getenv("PULSAR_URL", "pulsar://localhost:6650")
        self.cliente = pulsar.Client(self.pulsar_url)

        # Inicializar servicios
        repositorio_marca = RepositorioMarcaSQLAlchemy()
        repositorio_campana = RepositorioCampanaMarcaSQLAlchemy()
        self.servicio = ServicioMarca(repositorio_marca, repositorio_campana)

    async def consumir_eventos_campana(self, topico: str, suscripcion: str):
        try:
            # Crear esquema Avro para eventos de campaña
            schema = AvroSchema({
                "type": "record",
                "name": "EventoCampana",
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

            # Crear consumidor
            consumidor = self.cliente.subscribe(
                topico, suscripcion, schema=schema)

            print(f"[MARCA] Consumiendo eventos del tópico {topico}...")

            while True:
                try:
                    mensaje = consumidor.receive(timeout_millis=1000)
                    if mensaje:
                        evento_data = mensaje.value()
                        print(f"[MARCA] Evento recibido: {evento_data}")

                        # Procesar evento según el tipo
                        await self._procesar_evento_campana(evento_data)

                        # Confirmar mensaje
                        consumidor.acknowledge(mensaje)

                except pulsar.Timeout:
                    # Timeout normal, continuar
                    continue
                except Exception as e:
                    print(f"[MARCA] Error procesando mensaje: {e}")
                    consumidor.negative_acknowledge(mensaje)

        except Exception as e:
            print(f"[MARCA] Error en consumidor: {e}")
        finally:
            if 'consumidor' in locals():
                consumidor.close()

    async def _procesar_evento_campana(self, evento_data):
        try:
            # Determinar tipo de evento por los campos presentes
            if 'nombre' in evento_data and 'descripcion' in evento_data:
                # Es un evento de campaña creada
                print(
                    f"[MARCA] Procesando campaña creada: {evento_data['nombre']}")
                campana = self.servicio.procesar_campana_creada(evento_data)
                print(f"[MARCA] Campaña procesada y guardada: {campana.id}")
            elif 'fecha_inicio' in evento_data:
                # Es un evento de campaña iniciada
                print(
                    f"[MARCA] Procesando campaña iniciada: {evento_data['id_campana']}")
                campana = self.servicio.procesar_campana_iniciada(evento_data)
                if campana:
                    print(f"[MARCA] Campaña actualizada: {campana.id}")
                else:
                    print(f"[MARCA] Campaña no encontrada para actualizar")
        except Exception as e:
            print(f"[MARCA] Error procesando evento: {e}")


async def iniciar_consumidores():
    consumidor = ConsumidorEventosMarca()

    # Crear tareas para consumir eventos de campaña
    tareas = [
        asyncio.create_task(consumidor.consumir_eventos_campana(
            "eventos-campana", "marca-subscription")),
    ]

    # Ejecutar todas las tareas
    await asyncio.gather(*tareas)
