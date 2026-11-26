"""Reserva: integra cliente, servicio, duración y ciclo de vida."""
from models.entidad import Entidad
from models.cliente import Cliente
from models.servicio import Servicio
from exceptions.excepciones import (
    ReservaInvalidaError, ServicioInvalidoError, ServicioNoDisponibleError,
    OperacionNoPermitidaError, CalculoInconsistenteError,
)
from utils.logger import obtener_logger

log = obtener_logger()


class Reserva(Entidad):
    """Reserva con estados PENDIENTE, CONFIRMADA, PROCESADA y CANCELADA."""

    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"

    def __init__(self, cliente, servicio, duracion):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio válido.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"'{servicio.nombre}' no está disponible.")
        # La validación se convierte en ReservaInvalidaError conservando la causa original.
        try:
            servicio.validar_parametros(duracion)
        except ServicioInvalidoError as error:
            raise ReservaInvalidaError(
                f"La duración o cantidad de la reserva no es válida para '{servicio.nombre}'."
            ) from error
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = self.PENDIENTE
        self._total = None
        log.info("Reserva #%s creada en estado %s", self.id, self._estado)

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def total(self):
        return self._total

    def confirmar(self):
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Solo se confirma una reserva PENDIENTE (estado actual: {self._estado})."
            )
        self._servicio.validar_disponibilidad()
        self._estado = self.CONFIRMADA
        log.info("Reserva #%s confirmada", self.id)
        return f"Reserva #{self.id} confirmada."

    def cancelar(self):
        if self._estado == self.PROCESADA:
            raise OperacionNoPermitidaError("No se puede cancelar una reserva ya procesada.")
        if self._estado == self.CANCELADA:
            return f"La reserva #{self.id} ya estaba cancelada."
        self._estado = self.CANCELADA
        log.info("Reserva #%s cancelada", self.id)
        return f"Reserva #{self.id} cancelada."

    def procesar(self, impuesto=0.19, descuento=0.0):
        """Calcula el total; incorpora try/except/else/finally y encadenamiento."""
        if self._estado != self.CONFIRMADA:
            raise OperacionNoPermitidaError("Solo se procesan reservas CONFIRMADAS.")
        try:
            self._servicio.validar_disponibilidad()
            total = self._servicio.calcular_costo(
                self._duracion, impuesto=impuesto, descuento=descuento
            )
        except (ServicioInvalidoError, ServicioNoDisponibleError, CalculoInconsistenteError) as error:
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva #{self.id}."
            ) from error
        else:
            self._total = total
            self._estado = self.PROCESADA
            log.info("Reserva #%s procesada. Total: %.2f", self.id, total)
            return total
        finally:
            log.info("Fin del intento de procesamiento de la reserva #%s", self.id)

    def describir(self):
        total = f"${self._total:,.2f}" if self._total is not None else "sin calcular"
        return (f"Reserva #{self.id}: {self._cliente.nombre} -> {self._servicio.nombre} "
                f"x {self._duracion} | [{self._estado}] | Total: {total}")
