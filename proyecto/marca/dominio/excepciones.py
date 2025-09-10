class MarcaExcepcion(Exception):
    pass


class MarcaNoEncontradaExcepcion(MarcaExcepcion):
    def __init__(self, id_marca):
        self.id_marca = id_marca
        super().__init__(f"Marca con id {id_marca} no encontrada")


class CampanaNoEncontradaExcepcion(MarcaExcepcion):
    def __init__(self, id_campana):
        self.id_campana = id_campana
        super().__init__(f"Campana con id {id_campana} no encontrada")
