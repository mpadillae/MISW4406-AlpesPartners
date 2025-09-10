from abc import ABC, abstractmethod


class ReglaNegocio(ABC):
    @abstractmethod
    def es_valido(self) -> bool:
        pass


class EventoDebeTenerTipoValido(ReglaNegocio):
    def __init__(self, tipo_evento: str):
        self.tipo_evento = tipo_evento

    def es_valido(self) -> bool:
        tipos_validos = ["vista", "clic", "conversion",
                         "engagement", "compartir", "comentario"]
        return self.tipo_evento in tipos_validos


class MetricasDebenSerPositivas(ReglaNegocio):
    def __init__(self, metricas: dict):
        self.metricas = metricas

    def es_valido(self) -> bool:
        for key, value in self.metricas.items():
            if isinstance(value, (int, float)) and value < 0:
                return False
        return True
