import pulsar
from pulsar.schema import *

from alpesPartners.modulos.vuelos.infraestructura.schema.v1.eventos import EventoReservaCreada, ReservaCreadaPayload
from alpesPartners.modulos.vuelos.infraestructura.schema.v1.comandos import ComandoCrearReserva, ComandoCrearReservaPayload
from alpesPartners.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.fromtimestamp(0, datetime.UTC)


def unix_time_millis(dt):
    # Ensure both datetimes have the same timezone awareness
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.UTC)
    epoch_aware = epoch.replace(
        tzinfo=datetime.UTC) if epoch.tzinfo is None else epoch
    return (dt - epoch_aware).total_seconds() * 1000.0


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = ReservaCreadaPayload(
            id_reserva=str(evento.id_reserva),
            id_cliente=str(evento.id_cliente),
            estado=str(evento.estado),
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        evento_integracion = EventoReservaCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico,
                               AvroSchema(EventoReservaCreada))

    def publicar_comando(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = ComandoCrearReservaPayload(
            id_usuario=str(comando.id_usuario)
            # agregar itinerarios
        )
        comando_integracion = ComandoCrearReserva(data=payload)
        self._publicar_mensaje(comando_integracion, topico,
                               AvroSchema(ComandoCrearReserva))
