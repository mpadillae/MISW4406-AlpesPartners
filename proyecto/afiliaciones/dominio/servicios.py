from typing import List
import uuid
from .entidades import Campana
from .repositorios import RepositorioCampana
from .reglas import PresupuestoDebeSerPositivo, CampanaDebeTenerNombre
from .excepciones import PresupuestoInvalidoExcepcion, EstadoCampanaInvalidoExcepcion
from .objetos_valor import TipoCampana


class ServicioCampana:
    def __init__(self, repositorio: RepositorioCampana):
        self.repositorio = repositorio

    def crear_campana(self, id_marca: uuid.UUID, nombre: str, descripcion: str,
                      tipo: str, presupuesto: float) -> Campana:
        # Validar reglas de negocio
        if not PresupuestoDebeSerPositivo(presupuesto).es_valido():
            raise PresupuestoInvalidoExcepcion(presupuesto)

        if not CampanaDebeTenerNombre(nombre).es_valido():
            raise ValueError("El nombre de la campaña es requerido")

        # Crear entidad
        campana = Campana(
            id_marca=id_marca,
            nombre=nombre,
            descripcion=descripcion,
            tipo=TipoCampana(tipo),
            presupuesto=presupuesto
        )

        # Guardar en repositorio
        return self.repositorio.agregar(campana)

    def iniciar_campana(self, id_campana: uuid.UUID) -> Campana:
        campana = self.repositorio.obtener_por_id(id_campana)
        if not campana:
            raise ValueError(f"Campaña {id_campana} no encontrada")

        campana.iniciar_campana()
        return self.repositorio.actualizar(campana)

    def obtener_campana(self, id_campana: uuid.UUID) -> Campana:
        campana = self.repositorio.obtener_por_id(id_campana)
        if not campana:
            raise ValueError(f"Campaña {id_campana} no encontrada")
        return campana

    def obtener_todas_campanas(self) -> List[Campana]:
        return self.repositorio.obtener_todas()
