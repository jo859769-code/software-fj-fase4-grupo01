"""Excepciones del sistema Software FJ."""
from .excepciones import (
    SoftwareFJError, ClienteInvalidoError, ServicioInvalidoError,
    ServicioNoDisponibleError, ReservaInvalidaError,
    OperacionNoPermitidaError, CalculoInconsistenteError,
)

__all__ = [
    "SoftwareFJError", "ClienteInvalidoError", "ServicioInvalidoError",
    "ServicioNoDisponibleError", "ReservaInvalidaError",
    "OperacionNoPermitidaError", "CalculoInconsistenteError",
]
