from abc import ABC, abstractmethod
from typing import Any


class Query(ABC):
    pass


class ManejadorQuery(ABC):
    @abstractmethod
    async def ejecutar(self, query: Query) -> Any:
        pass
