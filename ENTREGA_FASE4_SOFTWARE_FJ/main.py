"""Simulación del Sistema Integral de Software FJ. Ejecutar con: python main.py"""
from models.cliente import Cliente
from models.reserva import Reserva
from services.reserva_salas import ReservaSala
from services.alquiler_equipos import AlquilerEquipo
from services.asesoria import Asesoria
from exceptions.excepciones import SoftwareFJError
from utils.logger import obtener_logger

log = obtener_logger()
clientes = []
servicios = []
reservas = []


def ejecutar(numero, descripcion, accion):
    """Ejecuta una operación aislada; un fallo no detiene las siguientes."""
    print(f"\nOperación {numero:02d}: {descripcion}")
    try:
        resultado = accion()
    except SoftwareFJError as error:
        causa = f" | Causa original: {error.__cause__}" if error.__cause__ else ""
        print(f"  ERROR CONTROLADO: {type(error).__name__}: {error}{causa}")
        log.error("Operación %02d - %s: %s%s", numero, type(error).__name__, error, causa)
    except Exception as error:
        print(f"  ERROR INESPERADO: {type(error).__name__}: {error}")
        log.exception("Operación %02d - error inesperado en %s", numero, descripcion)
    else:
        print(f"  CORRECTO: {resultado}")
        log.info("Operación %02d - %s - resultado: %s", numero, descripcion, resultado)
    finally:
        print("  Fin de la operación.")
        log.info("Operación %02d finalizada: %s", numero, descripcion)


def registrar_cliente(nombre, documento, correo):
    cliente = Cliente(nombre, documento, correo)
    clientes.append(cliente)
    return cliente


def registrar_servicio(servicio):
    servicios.append(servicio)
    return servicio


def crear_reserva(cliente, servicio, duracion):
    reserva = Reserva(cliente, servicio, duracion)
    reservas.append(reserva)
    return reserva


def confirmar_y_procesar(reserva, impuesto=0.19, descuento=0.0):
    reserva.confirmar()
    total = reserva.procesar(impuesto=impuesto, descuento=descuento)
    return f"{reserva.describir()} | Total calculado: ${total:,.2f}"


def crear_cliente_valido():
    return registrar_cliente("Ana Gómez", "1065123456", "ana@correo.com").describir()


def crear_sala_valida():
    return registrar_servicio(ReservaSala("Sala Andes", 80000, 12)).describir()


def crear_equipo_y_asesoria():
    equipo = registrar_servicio(AlquilerEquipo("Portátil", 45000, 5))
    asesoria = registrar_servicio(Asesoria("Python POO", 120000, "avanzada"))
    return f"{equipo.describir()} | {asesoria.describir()}"


def reserva_sala_exitosa():
    cliente = clientes[0]
    sala = next(s for s in servicios if isinstance(s, ReservaSala))
    reserva = crear_reserva(cliente, sala, 3)
    return confirmar_y_procesar(reserva, impuesto=0.19)


def reserva_asesoria_con_descuento():
    cliente = clientes[0]
    asesoria = next(s for s in servicios if isinstance(s, Asesoria))
    reserva = crear_reserva(cliente, asesoria, 2)
    return confirmar_y_procesar(reserva, impuesto=0.19, descuento=0.10)


def reserva_con_impuesto_invalido():
    cliente = clientes[0]
    sala = next(s for s in servicios if isinstance(s, ReservaSala))
    reserva = crear_reserva(cliente, sala, 2)
    reserva.confirmar()
    # El método de Servicio genera ServicioInvalidoError; Reserva lo encadena.
    reserva.procesar(impuesto=1.50)


def mostrar_resumen():
    print("\n--- RESUMEN DEL SISTEMA ---")
    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios registrados: {len(servicios)}")
    print(f"Reservas almacenadas: {len(reservas)}")
    for reserva in reservas:
        print(" -", reserva.describir())
    return "Resumen generado."


def main():
    print("=" * 68)
    print("SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("SOFTWARE FJ | FASE 4 - PROGRAMACIÓN 213023")
    print("=" * 68)
    log.info("===== Inicio de la simulación Software FJ =====")

    operaciones = [
        ("Registrar cliente válido", crear_cliente_valido),
        ("Registrar cliente con correo inválido",
         lambda: registrar_cliente("Luis Pérez", "1065987654", "luis-correo")),
        ("Registrar cliente con documento inválido",
         lambda: registrar_cliente("Marta Ruiz", "12AB", "marta@correo.com")),
        ("Crear una sala de reuniones válida", crear_sala_valida),
        ("Crear equipo con tarifa negativa",
         lambda: registrar_servicio(AlquilerEquipo("Proyector", -5000, 3))),
        ("Crear equipo y asesoría válidos", crear_equipo_y_asesoria),
        ("Crear, confirmar y procesar reserva de sala (3 h + IVA)", reserva_sala_exitosa),
        ("Crear, confirmar y procesar asesoría con descuento", reserva_asesoria_con_descuento),
        ("Intentar reserva de sala durante 12 horas",
         lambda: crear_reserva(clientes[0], next(s for s in servicios if isinstance(s, ReservaSala)), 12)),
        ("Intentar reservar equipo no disponible",
         lambda: reservar_equipo_no_disponible()),
        ("Intentar cancelar reserva ya procesada", lambda: reservas[0].cancelar()),
        ("Intentar crear reserva sin objeto Cliente",
         lambda: crear_reserva(None, next(s for s in servicios if isinstance(s, ReservaSala)), 2)),
        ("Procesar reserva con porcentaje de impuesto inválido", reserva_con_impuesto_invalido),
        ("Mostrar resumen final", mostrar_resumen),
    ]

    # La indisponibilidad se activa justo antes de la operación 10.
    for numero, (descripcion, accion) in enumerate(operaciones, start=1):
        if numero == 10:
            equipo = next(s for s in servicios if isinstance(s, AlquilerEquipo))
            equipo.cambiar_disponibilidad(False)
        ejecutar(numero, descripcion, accion)

    print("\nLa simulación finalizó. Los errores controlados fueron registrados en logs/software_fj.log.")
    log.info("===== Fin de la simulación Software FJ =====")


def reservar_equipo_no_disponible():
    cliente = clientes[0]
    equipo = next(s for s in servicios if isinstance(s, AlquilerEquipo))
    return crear_reserva(cliente, equipo, 2).describir()


if __name__ == "__main__":
    main()
