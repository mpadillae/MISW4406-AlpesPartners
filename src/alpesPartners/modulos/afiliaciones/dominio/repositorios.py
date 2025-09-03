""" Interfaces para los repositorios del dominio de afiliaciones

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de afiliaciones y marketing de influencers

"""

from abc import ABC
from alpespartners.seedwork.dominio.repositorios import Repositorio

class RepositorioCampanas(Repositorio, ABC):
    ...

class RepositorioInfluencers(Repositorio, ABC):
    ...