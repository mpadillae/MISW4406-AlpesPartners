from dataclasses import dataclass
import uuid
from .base import Comando


@dataclass
class CrearCampana(Comando):
    id_marca: uuid.UUID
    nombre: str
    descripcion: str
    tipo: str
    presupuesto: float
