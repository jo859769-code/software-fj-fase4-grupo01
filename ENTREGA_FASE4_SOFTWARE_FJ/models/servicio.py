"""Clase abstracta Servicio: contrato común de los servicios ofrecidos."""
from abc import abstractmethod
import math
from models.entidad import Entidad
from exceptions.excepciones import (
    ServicioInvalidoError, ServicioNoDisponibleError, CalculoInconsistenteError,
)


class Servicio(Entidad):
    """Servicio base con tarifa, disponibilidad y cálculo común."""

    def __init__(self, nombre, tarifa_base, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre válido.")
        if (not isinstance(tarifa_base, (int, float)) or isinstance(tarifa_base, bool)
                or not math.isfinite(tarifa_base) or tarifa_base <= 0):
            raise ServicioInvalidoError("La tarifa base debe ser un número finito mayor que cero.")
        if not isinstance(disponible, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        self._disponible = estado

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    @abstractmethod
    def costo_base(self, cantidad):
        """Calcula el costo sin impuestos ni descuentos."""
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, cantidad):
        """Comprueba las reglas de duración o cantidad del servicio."""
        raise NotImplementedError

    def calcular_costo(self, cantidad, impuesto=0.0, descuento=0.0):
        """Permite calcular costo base, con impuesto, con descuento o ambos.

        Los porcentajes se expresan como fracciones: 0.19 equivale a 19 %.
        """
        self.validar_disponibilidad()
        self.validar_parametros(cantidad)
        for etiqueta, valor in (("impuesto", impuesto), ("descuento", descuento)):
            if (not isinstance(valor, (int, float)) or isinstance(valor, bool)
                    or not math.isfinite(valor) or not 0 <= valor <= 1):
                raise ServicioInvalidoError(
                    f"El {etiqueta} debe expresarse como fracción entre 0 y 1."
                )
        subtotal = self.costo_base(cantidad) * (1 - descuento)
        total = round(subtotal * (1 + impuesto), 2)
        if not math.isfinite(total) or total <= 0:
            raise CalculoInconsistenteError(f"Costo calculado inválido: {total}")
        return total
