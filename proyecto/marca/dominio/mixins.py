from abc import ABC, abstractmethod


class MixinValidacion(ABC):
    @abstractmethod
    def validar(self) -> bool:
        pass


class MixinEventos:
    def __init__(self):
        self._eventos = []

    def agregar_evento(self, evento):
        self._eventos.append(evento)

    def limpiar_eventos(self):
        self._eventos.clear()

    def obtener_eventos(self):
        return self._eventos.copy()
