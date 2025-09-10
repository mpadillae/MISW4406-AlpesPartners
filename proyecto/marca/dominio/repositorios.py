from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from .entidades import Marca, CampanaMarca


class RepositorioMarca(ABC):
    @abstractmethod
    def obtener_por_id(self, id_marca: uuid.UUID) -> Optional[Marca]:
        pass

    @abstractmethod
    def obtener_todas(self) -> List[Marca]:
        pass

    @abstractmethod
    def agregar(self, marca: Marca) -> Marca:
        pass

    @abstractmethod
    def actualizar(self, marca: Marca) -> Marca:
        pass


class RepositorioCampanaMarca(ABC):
    @abstractmethod
    def obtener_por_id(self, id_campana: uuid.UUID) -> Optional[CampanaMarca]:
        pass

    @abstractmethod
    def obtener_por_marca(self, id_marca: uuid.UUID) -> List[CampanaMarca]:
        pass

    @abstractmethod
    def obtener_todas(self) -> List[CampanaMarca]:
        pass

    @abstractmethod
    def agregar(self, campana: CampanaMarca) -> CampanaMarca:
        pass

    @abstractmethod
    def actualizar(self, campana: CampanaMarca) -> CampanaMarca:
        pass
