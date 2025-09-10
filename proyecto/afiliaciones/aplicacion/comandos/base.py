from abc import ABC, abstractmethod
from typing import Any


class Comando(ABC):
    pass


class ManejadorComando(ABC):
    @abstractmethod
    async def ejecutar(self, comando: Comando) -> Any:
        pass
