"""Mixins del dominio de afiliaciones

En este archivo usted encontrará los mixins para diferentes funcionalidades
reusables en el dominio de afiliaciones

"""

from .entidades import Influencer, Campana

class FiltradoInfluencersMixin:

    def filtrar_mejores_influencers(self, influencers: list[Influencer]) -> list[Influencer]:
        # Lógica compleja para filtrar influencers basado en métricas de engagement, alcance, etc.
        return sorted(influencers, key=lambda inf: inf.calcular_alcance_total(), reverse=True)

class OptimizacionCampanaMixin:

    def optimizar_presupuesto_campana(self, campana: Campana) -> Campana:
        # Lógica para optimizar el presupuesto de la campaña
        return campana