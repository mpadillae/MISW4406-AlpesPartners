"""Reglas de negocio del dominio de afiliaciones

En este archivo usted encontrará reglas de negocio del dominio de afiliaciones y marketing de influencers

"""

from alpespartners.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import Influencer, PresupuestoCampana
from datetime import datetime


class MinimoUnInfluencer(ReglaNegocio):
    """Regla que valida que una campaña tenga al menos un influencer asociado"""

    influencers: list[Influencer]

    def __init__(self, influencers, mensaje='Una campaña debe tener al menos un influencer asociado'):
        super().__init__(mensaje)
        self.influencers = influencers

    def es_valido(self) -> bool:
        return len(self.influencers) > 0 and all(isinstance(inf, Influencer) for inf in self.influencers)


class PresupuestoValido(ReglaNegocio):
    """Regla que valida que el presupuesto de la campaña sea positivo"""

    presupuesto: PresupuestoCampana

    def __init__(self, presupuesto, mensaje='El presupuesto de la campaña debe ser mayor a cero'):
        super().__init__(mensaje)
        self.presupuesto = presupuesto

    def es_valido(self) -> bool:
        return self.presupuesto.valor > 0


class FechasValidas(ReglaNegocio):
    """Regla que valida que la fecha de inicio sea anterior a la fecha de fin"""

    fecha_inicio: datetime
    fecha_fin: datetime

    def __init__(self, fecha_inicio, fecha_fin, mensaje='La fecha de inicio debe ser anterior a la fecha de fin'):
        super().__init__(mensaje)
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def es_valido(self) -> bool:
        return self.fecha_inicio < self.fecha_fin


class InfluencerActivo(ReglaNegocio):
    """Regla que valida que un influencer tenga al menos una red social activa"""

    influencer: Influencer

    def __init__(self, influencer, mensaje='El influencer debe tener al menos una red social activa'):
        super().__init__(mensaje)
        self.influencer = influencer

    def es_valido(self) -> bool:
        return len(self.influencer.redes_sociales) > 0


class AlcanceMinimoInfluencer(ReglaNegocio):
    """Regla que valida que un influencer tenga un alcance mínimo"""

    influencer: Influencer
    alcance_minimo: int

    def __init__(self, influencer, alcance_minimo=1000, mensaje='El influencer debe tener al menos 1000 seguidores'):
        super().__init__(mensaje)
        self.influencer = influencer
        self.alcance_minimo = alcance_minimo

    def es_valido(self) -> bool:
        alcance_total = self.influencer.calcular_alcance_total()
        return alcance_total >= self.alcance_minimo 