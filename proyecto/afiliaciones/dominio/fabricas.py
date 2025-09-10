from .entidades import Campana
from .objetos_valor import TipoCampana, EstadoCampana
import uuid


class FabricaCampana:
    @staticmethod
    def crear_campana(id_marca: uuid.UUID, nombre: str, descripcion: str,
                      tipo: str, presupuesto: float) -> Campana:
        tipo_enum = TipoCampana(tipo) if tipo in [
            t.value for t in TipoCampana] else TipoCampana.INFLUENCER

        return Campana(
            id_marca=id_marca,
            nombre=nombre,
            descripcion=descripcion,
            tipo=tipo_enum,
            presupuesto=presupuesto
        )
