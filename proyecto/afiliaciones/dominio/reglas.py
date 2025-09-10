from abc import ABC, abstractmethod
from typing import Any


class ReglaNegocio(ABC):
    @abstractmethod
    def es_valido(self) -> bool:
        pass


class PresupuestoDebeSerPositivo(ReglaNegocio):
    def __init__(self, presupuesto: float):
        self.presupuesto = presupuesto

    def es_valido(self) -> bool:
        return self.presupuesto > 0


class CampanaDebeTenerNombre(ReglaNegocio):
    def __init__(self, nombre: str):
        self.nombre = nombre

    def es_valido(self) -> bool:
        return self.nombre is not None and len(self.nombre.strip()) > 0
