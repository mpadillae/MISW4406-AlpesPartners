from .repositorios import RepositorioMetricasCampanaSQLAlchemy, RepositorioEventoTrackingSQLAlchemy
from dominio.repositorios import RepositorioMetricasCampana, RepositorioEventoTracking


class FabricaRepositorio:
    @staticmethod
    def crear_repositorio_metricas_campana() -> RepositorioMetricasCampana:
        return RepositorioMetricasCampanaSQLAlchemy()

    @staticmethod
    def crear_repositorio_evento_tracking() -> RepositorioEventoTracking:
        return RepositorioEventoTrackingSQLAlchemy()
