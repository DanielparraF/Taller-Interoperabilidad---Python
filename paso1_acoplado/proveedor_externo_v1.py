"""
Paso 1 — Proveedor Externo V1 (simulado)

Interfaz real del proveedor. No se puede modificar.
  executeTransaction(user, amount, currency)
    → { resultCode, authId, timestamp }
"""


class ProveedorExternoV1:
    """
    Proveedor de pagos externo — Versión 1.
    Interfaz original antes de cualquier cambio.
    """

    def executeTransaction(self, user: str, amount: float, currency: str) -> dict:
        return {
            "resultCode": "00",
            "authId":     "AUTH-9821",
            "timestamp":  "2026-03-16T10:00:00Z"
        }
