"""
Paso 3 — Contrato interno estable

Define la interfaz que el sistema principal usará SIEMPRE,
sin importar qué proveedor externo esté detrás.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ResultadoPago:
    """
    Respuesta normalizada del contrato interno.
    Siempre tiene la misma forma, sin importar el proveedor.
    """
    estado: str               # "APROBADO" | "RECHAZADO"
    codigo_autorizacion: str  # código devuelto por el proveedor


class ServicioPago(ABC):
    """
    Contrato estable que el sistema principal utiliza siempre.
    Ninguna clase fuera de los adaptadores conoce los proveedores reales.
    """

    @abstractmethod
    def procesarPago(self, cliente_id: str, monto: float) -> ResultadoPago:
        """
        Procesa un pago y retorna un ResultadoPago normalizado.

        Args:
            cliente_id: Identificador del cliente en el sistema interno.
            monto:      Monto a cobrar.

        Returns:
            ResultadoPago con estado y codigo_autorizacion.
        """
