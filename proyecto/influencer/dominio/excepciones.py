class InfluencerExcepcion(Exception):
    pass


class InfluencerNoEncontradoExcepcion(InfluencerExcepcion):
    def __init__(self, id_influencer):
        self.id_influencer = id_influencer
        super().__init__(f"Influencer con id {id_influencer} no encontrado")


class CampanaNoEncontradaExcepcion(InfluencerExcepcion):
    def __init__(self, id_campana):
        self.id_campana = id_campana
        super().__init__(f"Campana con id {id_campana} no encontrada")
