""" Excepciones del dominio de afiliaciones

En este archivo usted encontrará los Excepciones relacionadas
al dominio de afiliaciones y marketing de influencers

"""

from alpespartners.seedwork.dominio.excepciones import ExcepcionFabrica

class TipoObjetoNoExisteEnDominioAfiliacionesExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de afiliaciones'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)