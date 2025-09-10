from .repositorios import RepositorioInfluencerSQLAlchemy, RepositorioCampanaInfluencerSQLAlchemy
from dominio.repositorios import RepositorioInfluencer, RepositorioCampanaInfluencer


class FabricaRepositorio:
    @staticmethod
    def crear_repositorio_influencer() -> RepositorioInfluencer:
        return RepositorioInfluencerSQLAlchemy()

    @staticmethod
    def crear_repositorio_campana_influencer() -> RepositorioCampanaInfluencer:
        return RepositorioCampanaInfluencerSQLAlchemy()
