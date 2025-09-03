from alpespartners.modulos.afiliaciones.dominio.eventos import CampanaCreada
from alpespartners.seedwork.aplicacion.handlers import Handler
from alpespartners.modulos.afiliaciones.infraestructura.despachadores import Despachador


class HandlerCampanaIntegracion(Handler):

    @staticmethod
    def handle_campana_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-campana')
