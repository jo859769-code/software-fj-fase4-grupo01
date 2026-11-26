"""Clase abstracta que representa las entidades generales del sistema."""
from abc import ABC, abstractmethod
from itertools import count


class Entidad(ABC):
    """Entidad con identificador único durante la ejecución."""

    _contador = count(1)

    def __init__(self):
        self._id = next(Entidad._contador)

    @property
    def id(self):
        """Identificador de solo lectura."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad concreta debe implementar su descripción."""
        raise NotImplementedError

    def __str__(self):
        return self.describir()
