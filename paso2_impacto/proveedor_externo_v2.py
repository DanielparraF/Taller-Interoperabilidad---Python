"""
Paso 2 — Proveedor Externo V2 (interfaz cambiada)

El proveedor renombró todo sin previo aviso:
  executeTransaction  →  processPayment
  user                →  customerId
  amount              →  totalAmount
  currency            →  currencyCode
  resultCode          →  status  ("SUCCESS" | "FAILED")
  authId              →  confirmationCode
  + nuevo campo:         transactionId
"""


class ProveedorExternoV2:
    """
    Proveedor de pagos externo — Versión 2.
    Interfaz completamente renombrada respecto a V1.
    """

    def processPayment(self, customerId: str, totalAmount: float, currencyCode: str) -> dict:
        return {
            "status":          "SUCCESS",
            "confirmationCode": "CONF-7734",
            "transactionId":   "TXN-0042"
        }
