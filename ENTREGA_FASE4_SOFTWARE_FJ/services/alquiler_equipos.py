"""Servicio especializado de alquiler de equipos por días."""
from models.servicio import Servicio
from exceptions.excepciones import ServicioInvalidoError


class AlquilerEquipo(Servicio):
    """Alquiler de equipos tecnológicos, con inventario disponible."""

    def __init__(self, nombre, tarifa_dia, unidades_disponibles, disponible=True):
        super().__init__(nombre, tarifa_dia, disponible)
        if (not isinstance(unidades_disponibles, int) or isinstance(unidades_disponibles, bool)
                or unidades_disponibles <= 0):
            raise ServicioInvalidoError("Las unidades disponibles deben ser un entero positivo.")
        self._unidades = unidades_disponibles

    @property
    def unidades_disponibles(self):
        return self._unidades

    def validar_parametros(self, dias):
        if not isinstance(dias, int) or isinstance(dias, bool) or not 1 <= dias <= 30:
            raise ServicioInvalidoError("El alquiler de equipos es de 1 a 30 días completos.")

    def costo_base(self, dias):
        # Política de ejemplo: desde siete días se aplica un 10 % de descuento por volumen.
        factor = 0.90 if dias >= 7 else 1.0
        return self._tarifa_base * dias * factor

    def describir(self):
        return (f"Equipo '{self.nombre}' - ${self._tarifa_base:,.0f}/día "
                f"({self.unidades_disponibles} unidades)")
