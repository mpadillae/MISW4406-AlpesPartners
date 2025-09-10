from typing import List
import uuid
from .entidades import Marca, CampanaMarca
from .repositorios import RepositorioMarca, RepositorioCampanaMarca
from .eventos import CampanaProcesada, MarcaActualizada


class ServicioMarca:
    def __init__(self, repositorio_marca: RepositorioMarca, repositorio_campana: RepositorioCampanaMarca):
        self.repositorio_marca = repositorio_marca
        self.repositorio_campana = repositorio_campana

    def procesar_campana_creada(self, evento_data: dict) -> CampanaMarca:
        # Crear o actualizar campaña de marca
        campana = CampanaMarca()
        campana.procesar_campana_creada(evento_data)

        # Guardar en repositorio
        campana_guardada = self.repositorio_campana.agregar(campana)

        # Crear evento de dominio
        evento = CampanaProcesada(
            id_campana=campana_guardada.id_campana,
            id_marca=campana_guardada.id_marca,
            nombre_campana=campana_guardada.nombre_campana,
            estado=campana_guardada.estado,
            fecha_procesamiento=campana_guardada.fecha_creacion
        )
        campana_guardada.agregar_evento(evento)

        return campana_guardada

    def procesar_campana_iniciada(self, evento_data: dict) -> CampanaMarca:
        # Buscar campaña existente
        id_campana = uuid.UUID(evento_data.get('id_campana'))
        campana = self.repositorio_campana.obtener_por_id(id_campana)

        if campana:
            campana.procesar_campana_iniciada(evento_data)
            return self.repositorio_campana.actualizar(campana)

        return None

    def obtener_campanas_por_marca(self, id_marca: uuid.UUID) -> List[CampanaMarca]:
        return self.repositorio_campana.obtener_por_marca(id_marca)

    def obtener_todas_campanas(self) -> List[CampanaMarca]:
        return self.repositorio_campana.obtener_todas()
