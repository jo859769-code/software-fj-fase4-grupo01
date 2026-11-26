"""Configuración centralizada del registro de eventos y errores."""
import logging
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_LOGS = RAIZ_PROYECTO / "logs"
ARCHIVO_LOG = RUTA_LOGS / "software_fj.log"


def obtener_logger(nombre="software_fj"):
    """Devuelve un logger que escribe en logs/software_fj.log."""
    RUTA_LOGS.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not logger.handlers:
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
    return logger
