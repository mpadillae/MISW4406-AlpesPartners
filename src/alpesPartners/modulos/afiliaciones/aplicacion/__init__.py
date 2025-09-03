from pydispatch import dispatcher

from .handlers import HandlerCampanaIntegracion

from alpespartners.modulos.afiliaciones.dominio.eventos import CampanaCreada

dispatcher.connect(HandlerCampanaIntegracion.handle_campana_creada,
                   signal=f'{CampanaCreada.__name__}Integracion')
