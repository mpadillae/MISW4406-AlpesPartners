from .entidades import Influencer, CampanaInfluencer
from .objetos_valor import PlataformaInfluencer, CategoriaInfluencer
import uuid


class FabricaInfluencer:
    @staticmethod
    def crear_influencer(nombre: str, plataforma: str, seguidores: int, categoria: str) -> Influencer:
        plataforma_enum = PlataformaInfluencer(plataforma) if plataforma in [
            p.value for p in PlataformaInfluencer] else PlataformaInfluencer.INSTAGRAM
        categoria_enum = CategoriaInfluencer(categoria) if categoria in [
            c.value for c in CategoriaInfluencer] else CategoriaInfluencer.OTROS

        return Influencer(
            nombre=nombre,
            plataforma=plataforma_enum.value,
            seguidores=seguidores,
            categoria=categoria_enum.value
        )


class FabricaCampanaInfluencer:
    @staticmethod
    def crear_campana_influencer(evento_data: dict) -> CampanaInfluencer:
        campana = CampanaInfluencer()
        campana.procesar_campana_creada(evento_data)
        return campana
