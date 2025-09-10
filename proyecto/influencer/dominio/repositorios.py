from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from .entidades import Influencer, CampanaInfluencer


class RepositorioInfluencer(ABC):
    @abstractmethod
    def obtener_por_id(self, id_influencer: uuid.UUID) -> Optional[Influencer]:
        pass

    @abstractmethod
    def obtener_por_categoria(self, categoria: str) -> List[Influencer]:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Influencer]:
        pass

    @abstractmethod
    def agregar(self, influencer: Influencer) -> Influencer:
        pass

    @abstractmethod
    def actualizar(self, influencer: Influencer) -> Influencer:
        pass


class RepositorioCampanaInfluencer(ABC):
    @abstractmethod
    def obtener_por_id(self, id_campana: uuid.UUID) -> Optional[CampanaInfluencer]:
        pass

    @abstractmethod
    def obtener_por_influencer(self, id_influencer: uuid.UUID) -> List[CampanaInfluencer]:
        pass

    @abstractmethod
    def obtener_todas(self) -> List[CampanaInfluencer]:
        pass

    @abstractmethod
    def agregar(self, campana: CampanaInfluencer) -> CampanaInfluencer:
        pass

    @abstractmethod
    def actualizar(self, campana: CampanaInfluencer) -> CampanaInfluencer:
        pass
