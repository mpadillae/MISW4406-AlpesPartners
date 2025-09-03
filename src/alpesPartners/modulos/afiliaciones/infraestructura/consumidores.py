import pulsar
import _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from alpespartners.modulos.afiliaciones.infraestructura.schema.v1.eventos import EventoCampanaCreada
from alpespartners.modulos.afiliaciones.infraestructura.schema.v1.comandos import ComandoCrearCampana
from alpespartners.seedwork.infraestructura import utils


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-campana', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='alpespartners-sub-eventos', schema=AvroSchema(EventoCampanaCreada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-campana', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='alpespartners-sub-comandos', schema=AvroSchema(ComandoCrearCampana))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
