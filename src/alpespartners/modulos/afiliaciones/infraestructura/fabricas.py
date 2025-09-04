""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de afiliaciones

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de afiliaciones

"""

from dataclasses import dataclass
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Repositorio
from alpespartners.modulos.afiliaciones.dominio.repositorios import RepositorioCampanas
from .repositorios import RepositorioCampanasPostgresql
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioCampanas.__class__:
            return RepositorioCampanasPostgresql()
        else:
            raise ExcepcionFabrica()
