# Plan de pruebas - Software FJ

Las siguientes operaciones deben ejecutarse de forma secuencial con `python main.py`. La tabla identifica qué se valida y qué resultado se espera.

| N.º | Operación | Clasificación | Resultado esperado |
|---:|---|---|---|
| 1 | Registrar cliente válido | Cliente válido | Cliente almacenado en la lista |
| 2 | Registrar cliente con correo inválido | Cliente inválido | `ClienteInvalidoError`; el programa continúa |
| 3 | Registrar cliente con documento no numérico | Cliente inválido | `ClienteInvalidoError`; el programa continúa |
| 4 | Crear sala válida | Servicio correcto | Objeto `ReservaSala` creado |
| 5 | Crear equipo con tarifa negativa | Servicio incorrecto | `ServicioInvalidoError`; no se almacena |
| 6 | Crear equipo y asesoría válidos | Servicios correctos | Dos servicios almacenados |
| 7 | Reservar sala 3 horas con IVA 19 % | Reserva exitosa | Total esperado: $285.600 |
| 8 | Reservar asesoría avanzada 2 horas con IVA 19 % y descuento 10 % | Reserva exitosa | Total esperado: $385.560 |
| 9 | Reservar sala durante 12 horas | Reserva fallida | `ReservaInvalidaError` encadenada a `ServicioInvalidoError` |
| 10 | Reservar equipo marcado no disponible | Reserva fallida | `ServicioNoDisponibleError` |
| 11 | Cancelar una reserva ya procesada | Operación no permitida | `OperacionNoPermitidaError` |
| 12 | Crear reserva sin un cliente válido | Reserva fallida | `ReservaInvalidaError` |
| 13 | Procesar reserva con impuesto fuera del rango permitido | Cálculo inválido | `ReservaInvalidaError` con `ServicioInvalidoError` como causa |
| 14 | Mostrar resumen final | Verificación | Listas y estados mostrados sin interrumpir la ejecución |

## Cálculos de comprobación

- Operación 7: 3 × $80.000 = $240.000; con IVA de 19 %: $240.000 × 1,19 = **$285.600**.
- Operación 8: 2 × $120.000 × 1,5 (nivel avanzado) = $360.000; con descuento de 10 %: $324.000; con IVA de 19 %: **$385.560**.

## Evidencia

Guardar una captura de la consola al finalizar `main.py` y otra del contenido de `logs/software_fj.log`. La captura debe corresponder a una ejecución real del código.
