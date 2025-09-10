from .repositorios import RepositorioMarcaSQLAlchemy, RepositorioCampanaMarcaSQLAlchemy
from dominio.repositorios import RepositorioMarca, RepositorioCampanaMarca


class FabricaRepositorio:
    @staticmethod
    def crear_repositorio_marca() -> RepositorioMarca:
        return RepositorioMarcaSQLAlchemy()

    @staticmethod
    def crear_repositorio_campana_marca() -> RepositorioCampanaMarca:
        return RepositorioCampanaMarcaSQLAlchemy()
