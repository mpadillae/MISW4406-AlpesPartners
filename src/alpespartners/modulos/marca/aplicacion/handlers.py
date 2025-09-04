

from alpespartners.modulos.afiliaciones.dominio.eventos import CampanaCreada
from alpespartners.seedwork.aplicacion.handlers import Handler

class HandlerCampanaDominio(Handler):

    @staticmethod
    def handle_campana_creada(evento):
        print('================ CAMPAÑA CREADA ===========')
        print('================ HOLA DESDE MODULO DE MARCA ===========')
        

    