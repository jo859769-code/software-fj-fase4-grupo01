"""Servicio especializado de asesoría."""
from models.servicio import Servicio
from exceptions.excepciones import ServicioInvalidoError

RECARGOS = {"basica": 1.0, "avanzada": 1.5, "experta": 2.0}


class Asesoria(Servicio):
    """Asesoría por hora con nivel de especialización."""

    def __init__(self, nombre, tarifa_hora, nivel, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(nivel, str) or nivel.lower() not in RECARGOS:
            raise ServicioInvalidoError(
                f"Nivel de asesoría desconocido: {nivel!r}. Use básica, avanzada o experta."
            )
        self._nivel = nivel.lower()

    @property
    def nivel(self):
        return self._nivel

    def validar_parametros(self, horas):
        if (not isinstance(horas, (int, float)) or isinstance(horas, bool)
                or not 0 < horas <= 40):
            raise ServicioInvalidoError("Las horas de asesoría deben ser mayores que 0 y hasta 40.")

    def costo_base(self, horas):
        return self._tarifa_base * horas * RECARGOS[self._nivel]

    def describir(self):
        return (f"Asesoría '{self.nombre}' nivel {self.nivel} - "
                f"${self._tarifa_base:,.0f}/hora")
