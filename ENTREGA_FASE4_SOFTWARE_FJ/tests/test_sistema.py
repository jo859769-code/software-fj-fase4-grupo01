"""Pruebas automáticas básicas de clases y reglas de negocio."""
import unittest
from models.cliente import Cliente
from models.reserva import Reserva
from services.reserva_salas import ReservaSala
from services.alquiler_equipos import AlquilerEquipo
from services.asesoria import Asesoria
from exceptions.excepciones import (
    ClienteInvalidoError, ReservaInvalidaError, ServicioNoDisponibleError,
    OperacionNoPermitidaError,
)


class TestSistemaSoftwareFJ(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente("Ana Gómez", "1065123456", "ana@correo.com")
        self.sala = ReservaSala("Sala Andes", 80000, 12)

    def test_cliente_enmascara_documento(self):
        self.assertEqual(self.cliente.documento, "****3456")

    def test_correo_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Luis Pérez", "1065987654", "correo-invalido")

    def test_calculo_sala_con_iva(self):
        self.assertEqual(self.sala.calcular_costo(3, impuesto=0.19), 285600.0)

    def test_calculo_con_descuento_e_iva(self):
        asesoria = Asesoria("Python POO", 120000, "avanzada")
        self.assertEqual(asesoria.calcular_costo(2, impuesto=0.19, descuento=0.10), 385560.0)

    def test_reserva_ciclo_de_vida(self):
        reserva = Reserva(self.cliente, self.sala, 3)
        reserva.confirmar()
        total = reserva.procesar()
        self.assertEqual(total, 285600.0)
        self.assertEqual(reserva.estado, Reserva.PROCESADA)

    def test_duracion_invalida_se_encadena(self):
        with self.assertRaises(ReservaInvalidaError) as contexto:
            Reserva(self.cliente, self.sala, 12)
        self.assertIsNotNone(contexto.exception.__cause__)

    def test_servicio_no_disponible(self):
        equipo = AlquilerEquipo("Portátil", 45000, 3, disponible=False)
        with self.assertRaises(ServicioNoDisponibleError):
            Reserva(self.cliente, equipo, 2)

    def test_no_cancelar_reserva_procesada(self):
        reserva = Reserva(self.cliente, self.sala, 2)
        reserva.confirmar()
        reserva.procesar()
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.cancelar()


if __name__ == "__main__":
    unittest.main(verbosity=2)
