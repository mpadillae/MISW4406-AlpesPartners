from .entidades import Marca, CampanaMarca
from .objetos_valor import CategoriaMarca
import uuid


class FabricaMarca:
    @staticmethod
    def crear_marca(nombre: str, categoria: str) -> Marca:
        categoria_enum = CategoriaMarca(categoria) if categoria in [
            c.value for c in CategoriaMarca] else CategoriaMarca.OTROS

        return Marca(
            nombre=nombre,
            categoria=categoria_enum.value
        )


class FabricaCampanaMarca:
    @staticmethod
    def crear_campana_marca(evento_data: dict) -> CampanaMarca:
        campana = CampanaMarca()
        campana.procesar_campana_creada(evento_data)
        return campana
