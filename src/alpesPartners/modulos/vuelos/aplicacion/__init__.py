from pydispatch import dispatcher

from .handlers import HandlerReservaIntegracion

from alpesPartners.modulos.vuelos.dominio.eventos import ReservaCreada

dispatcher.connect(HandlerReservaIntegracion.handle_reserva_creada,
                   signal=f'{ReservaCreada.__name__}Integracion')
