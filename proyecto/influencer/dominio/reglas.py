from abc import ABC, abstractmethod


class ReglaNegocio(ABC):
    @abstractmethod
    def es_valido(self) -> bool:
        pass


class InfluencerDebeTenerNombre(ReglaNegocio):
    def __init__(self, nombre: str):
        self.nombre = nombre

    def es_valido(self) -> bool:
        return self.nombre is not None and len(self.nombre.strip()) > 0


class InfluencerDebeTenerSeguidoresPositivos(ReglaNegocio):
    def __init__(self, seguidores: int):
        self.seguidores = seguidores

    def es_valido(self) -> bool:
        return self.seguidores >= 0
