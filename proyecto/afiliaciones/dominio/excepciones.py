class AfiliacionesExcepcion(Exception):
    pass


class CampanaNoEncontradaExcepcion(AfiliacionesExcepcion):
    def __init__(self, id_campana):
        self.id_campana = id_campana
        super().__init__(f"Campana con id {id_campana} no encontrada")


class EstadoCampanaInvalidoExcepcion(AfiliacionesExcepcion):
    def __init__(self, estado_actual, operacion):
        super().__init__(
            f"No se puede {operacion} una campaña en estado {estado_actual}")


class PresupuestoInvalidoExcepcion(AfiliacionesExcepcion):
    def __init__(self, presupuesto):
        super().__init__(f"El presupuesto {presupuesto} debe ser mayor a 0")
