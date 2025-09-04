import pulsar
from pulsar.schema import *

from alpespartners.modulos.afiliaciones.infraestructura.schema.v1.eventos import EventoCampanaCreada, CampanaCreadaPayload
from alpespartners.modulos.afiliaciones.infraestructura.schema.v1.comandos import ComandoCrearCampana, ComandoCrearCampanaPayload
from alpespartners.seedwork.infraestructura import utils

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
        payload = CampanaCreadaPayload(
            id_campana=str(evento.id_campana),
            id_marca=str(evento.id_marca),
            estado=str(evento.estado),
            fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
        )
        evento_integracion = EventoCampanaCreada(data=payload)
        self._publicar_mensaje(evento_integracion, topico,
                               AvroSchema(EventoCampanaCreada))

    def publicar_comando(self, comando, topico):
        payload = ComandoCrearCampanaPayload(
            id_marca=str(comando.id_marca)
            # agregar influencers
        )
        comando_integracion = ComandoCrearCampana(data=payload)
        self._publicar_mensaje(comando_integracion, topico,
                               AvroSchema(ComandoCrearCampana))
