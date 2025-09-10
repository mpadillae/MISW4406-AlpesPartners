from .repositorios import RepositorioCampanaSQLAlchemy
from .despachadores import Despachador
from dominio.repositorios import RepositorioCampana


class FabricaRepositorio:
    @staticmethod
    def crear_repositorio_campana() -> RepositorioCampana:
        return RepositorioCampanaSQLAlchemy()


class FabricaDespachador:
    @staticmethod
    def crear_despachador() -> Despachador:
        return Despachador()
