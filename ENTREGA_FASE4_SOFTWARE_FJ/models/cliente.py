"""Cliente con encapsulación de datos personales y validaciones."""
import re
from models.entidad import Entidad
from exceptions.excepciones import ClienteInvalidoError

PATRON_CORREO = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


class Cliente(Entidad):
    """Representa a una persona registrada en Software FJ."""

    def __init__(self, nombre, documento, correo):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def documento(self):
        """Muestra solo los últimos cuatro dígitos del documento."""
        return "****" + self.__documento[-4:]

    @documento.setter
    def documento(self, valor):
        if not isinstance(valor, (str, int)) or isinstance(valor, bool):
            raise ClienteInvalidoError("El documento debe contener únicamente dígitos.")
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError("El documento debe tener entre 6 y 12 dígitos.")
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not PATRON_CORREO.fullmatch(valor.strip()):
            raise ClienteInvalidoError(f"Correo electrónico no válido: {valor!r}")
        self.__correo = valor.strip().lower()

    def describir(self):
        return f"Cliente #{self.id}: {self.nombre} (documento {self.documento})"
