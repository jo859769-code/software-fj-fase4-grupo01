# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de la Fase 4 del curso Programación (código 213023), UNAD. Implementa en Python un sistema de simulación orientado a objetos para administrar clientes, servicios y reservas sin utilizar bases de datos. Los objetos y listas mantienen los datos en memoria; los archivos se utilizan únicamente para registrar eventos y errores.

**Repositorio:** https://github.com/jo859769-code/software-fj-fase4-grupo01

## Estructura

```text
software-fj-fase4-grupo01/
├── main.py
├── models/
│   ├── entidad.py
│   ├── cliente.py
│   ├── servicio.py
│   └── reserva.py
├── services/
│   ├── reserva_salas.py
│   ├── alquiler_equipos.py
│   └── asesoria.py
├── exceptions/
│   └── excepciones.py
├── utils/
│   └── logger.py
├── tests/
│   └── test_sistema.py
├── docs/
│   ├── Informe_Fase_4.docx
│   ├── Informe_Fase_4.pdf
│   ├── plan_pruebas.md
│   ├── salida_prueba_main.txt
│   ├── salida_pruebas_unitarias.txt
│   └── COMO_PUBLICAR_EN_GITHUB.md
├── logs/
│   └── .gitkeep
├── CONTRIBUCION_INDIVIDUAL.md
├── .gitignore
└── README.md
```

## Requisitos y ejecución

- Python 3.10 o superior.
- No requiere paquetes externos.
- Abrir la carpeta del repositorio en Visual Studio Code.
- Ejecutar `python main.py` (en Windows también se puede usar `py main.py`).
- El programa crea o actualiza `logs/software_fj.log` al ejecutarse.
- Ejecutar las pruebas con `python -m unittest discover -s tests -v`.

## Requisitos del ejercicio implementados

- Clases abstractas `Entidad` y `Servicio`.
- Herencia y especialización para clientes, servicios y reservas.
- Encapsulación y validación de datos personales del cliente.
- Polimorfismo mediante sobrescritura de métodos.
- Variantes de cálculo mediante parámetros opcionales en `calcular_costo(cantidad, impuesto=0.0, descuento=0.0)`. En Python se emplea esta estrategia en lugar de sobrecarga clásica de firmas. Los porcentajes se expresan como fracciones: `0.19` equivale a 19 %.
- Excepciones personalizadas y bloques `try/except/else/finally`.
- Encadenamiento de excepciones mediante `raise ... from ...`.
- Registro de eventos y errores en un archivo de log.
- Catorce operaciones simuladas, válidas y fallidas.

## Reglas de simulación

- Sala: entre 1 y 8 horas y capacidad positiva; tarifa por hora.
- Equipo: entre 1 y 30 días completos; unidades disponibles positivas; tarifa por día. Desde 7 días se aplica 10 % de descuento por volumen al costo base.
- Asesoría: más de 0 y hasta 40 horas; niveles `basica`, `avanzada` o `experta`.
- Impuesto y descuento: valores entre 0 y 1.
- Estados de reserva: `PENDIENTE`, `CONFIRMADA`, `PROCESADA` y `CANCELADA`.

Los valores son ficticios y se utilizan únicamente para la simulación académica.

## Pruebas

El plan de pruebas y las salidas de referencia están en `docs/`. Las pruebas unitarias verifican cálculos, validaciones, estados y excepciones. Los commits publicados deben representar cambios reales del autor; no se deben inventar participantes ni aportes.
