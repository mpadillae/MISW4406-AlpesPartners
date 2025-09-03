from alpesPartners.modulos.vuelos.dominio.eventos import ReservaCreada
from alpesPartners.seedwork.aplicacion.handlers import Handler
from alpesPartners.modulos.vuelos.infraestructura.despachadores import Despachador


class HandlerReservaIntegracion(Handler):

    @staticmethod
    def handle_reserva_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-reserva')
