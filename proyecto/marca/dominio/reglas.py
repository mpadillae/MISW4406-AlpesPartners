from abc import ABC, abstractmethod


class ReglaNegocio(ABC):
    @abstractmethod
    def es_valido(self) -> bool:
        pass


class MarcaDebeTenerNombre(ReglaNegocio):
    def __init__(self, nombre: str):
        self.nombre = nombre

    def es_valido(self) -> bool:
        return self.nombre is not None and len(self.nombre.strip()) > 0


class CampanaDebeTenerPresupuestoPositivo(ReglaNegocio):
    def __init__(self, presupuesto: float):
        self.presupuesto = presupuesto

    def es_valido(self) -> bool:
        return self.presupuesto > 0
