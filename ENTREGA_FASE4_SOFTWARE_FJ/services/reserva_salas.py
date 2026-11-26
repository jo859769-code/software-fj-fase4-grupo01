"""Servicio especializado de reserva de salas."""
from models.servicio import Servicio
from exceptions.excepciones import ServicioInvalidoError


class ReservaSala(Servicio):
    """Sala para reuniones, con tarifa por hora y capacidad definida."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    @property
    def capacidad(self):
        return self._capacidad

    def validar_parametros(self, horas):
        if (not isinstance(horas, (int, float)) or isinstance(horas, bool)
                or not 1 <= horas <= 8):
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 8 horas.")

    def costo_base(self, horas):
        return self._tarifa_base * horas

    def describir(self):
        return (f"Sala '{self.nombre}' ({self.capacidad} personas) - "
                f"${self._tarifa_base:,.0f}/hora")
