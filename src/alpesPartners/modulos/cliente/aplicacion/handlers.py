

from alpesPartners.modulos.vuelos.dominio.eventos import ReservaCreada
from alpesPartners.seedwork.aplicacion.handlers import Handler

class HandlerReservaDominio(Handler):

    @staticmethod
    def handle_reserva_creada(evento):
        print('================ RESERVA CREADA ===========')
        print('================ HOLA DESDE MODULO DE CLIENTE ===========')
        

    