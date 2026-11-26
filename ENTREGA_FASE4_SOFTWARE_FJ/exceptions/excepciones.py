"""Jerarquía de excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base: todas las excepciones del sistema heredan de ella."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos personales del cliente incorrectos o incompletos."""


class ServicioInvalidoError(SoftwareFJError):
    """Tarifa o parámetros de un servicio incorrectos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se intenta reservar un servicio que no está disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """La reserva no cumple las reglas del negocio."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se intenta realizar un cambio de estado no permitido."""


class CalculoInconsistenteError(SoftwareFJError):
    """El cálculo del costo produce un valor no válido."""
