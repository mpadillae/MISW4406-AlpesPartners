class TrackingExcepcion(Exception):
    pass


class MetricasNoEncontradasExcepcion(TrackingExcepcion):
    def __init__(self, id_campana):
        self.id_campana = id_campana
        super().__init__(f"Métricas para campaña {id_campana} no encontradas")


class EventoInvalidoExcepcion(TrackingExcepcion):
    def __init__(self, tipo_evento):
        self.tipo_evento = tipo_evento
        super().__init__(f"Tipo de evento {tipo_evento} no válido")
