from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from .entidades import Campana


class RepositorioCampana(ABC):
    @abstractmethod
    def obtener_por_id(self, id_campana: uuid.UUID) -> Optional[Campana]:
        pass

    @abstractmethod
    def obtener_todas(self) -> List[Campana]:
        pass

    @abstractmethod
    def agregar(self, campana: Campana) -> Campana:
        pass

    @abstractmethod
    def actualizar(self, campana: Campana) -> Campana:
        pass

    @abstractmethod
    def eliminar(self, id_campana: uuid.UUID) -> bool:
        pass
