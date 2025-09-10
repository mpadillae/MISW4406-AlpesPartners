import traceback
import pulsar
import _pulsar
from pulsar.schema import *
import os
import json
import asyncio
from datetime import datetime
from dominio.servicios import ServicioMarca
from infraestructura.schema.v1.eventos import EventoCampanaCreada
from .repositorios import RepositorioMarcaSQLAlchemy, RepositorioCampanaMarcaSQLAlchemy


class ConsumidorEventosMarca:
    def __init__(self):
        self.pulsar_url = os.getenv("PULSAR_URL", "pulsar://localhost:6650")

        # Inicializar servicios
        repositorio_marca = RepositorioMarcaSQLAlchemy()
        repositorio_campana = RepositorioCampanaMarcaSQLAlchemy()
        self.servicio = ServicioMarca(repositorio_marca, repositorio_campana)

    def consumir_eventos_campana(self, topico: str, suscripcion: str):
        try:
            cliente = pulsar.Client(self.pulsar_url)

            # Crear consumidor
            consumidor = cliente.subscribe(
                topico,
                consumer_type=_pulsar.ConsumerType.Shared,
                subscription_name=suscripcion,
                schema=AvroSchema(EventoCampanaCreada))

            while True:

                mensaje = consumidor.receive()
                evento_data = mensaje.value()

                print(f"[MARCA] Evento recibido: {evento_data.data}")

                # Procesar evento según el tipo
                self._procesar_evento_campana(evento_data.data.__dict__)

                # Confirmar mensaje

                consumidor.acknowledge(mensaje)

        except Exception as e:
            print(f"[MARCA] Error en consumidor: {e}")
            traceback.print_exc()

            if cliente:
                cliente.close()

    def _procesar_evento_campana(self, evento_data):

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
            traceback.print_exc()


def iniciar_consumidores():
    consumidor = ConsumidorEventosMarca()

    # Crear tareas para consumir eventos de campaña
    consumidor.consumir_eventos_campana(
        "eventos-campana", "marca-subscription")
