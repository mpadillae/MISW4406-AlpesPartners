from dataclasses import dataclass
import uuid
from .base import Comando


@dataclass
class IniciarCampana(Comando):
    id_campana: uuid.UUID
