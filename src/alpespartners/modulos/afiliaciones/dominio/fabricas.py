""" Fábricas para la creación de objetos del dominio de afiliaciones

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de afiliaciones y marketing de influencers

"""

from .entidades import Campana
from .reglas import MinimoUnInfluencer, PresupuestoValido
from .excepciones import TipoObjetoNoExisteEnDominioAfiliacionesExcepcion
from alpespartners.seedwork.dominio.repositorios import Mapeador, Repositorio
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass

@dataclass
class _FabricaCampana(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            campana: Campana = mapeador.dto_a_entidad(obj)

            self.validar_regla(MinimoUnInfluencer(campana.influencers))
            self.validar_regla(PresupuestoValido(campana.presupuesto))
            
            return campana

@dataclass
class FabricaAfiliaciones(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Campana.__class__:
            fabrica_campana = _FabricaCampana()
            return fabrica_campana.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioAfiliacionesExcepcion()

