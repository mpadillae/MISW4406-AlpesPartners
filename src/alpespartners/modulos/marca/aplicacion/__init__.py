from pydispatch import dispatcher
from .handlers import HandlerCampanaDominio

dispatcher.connect(HandlerCampanaDominio.handle_campana_creada, signal='CampanaCreadaDominio')
