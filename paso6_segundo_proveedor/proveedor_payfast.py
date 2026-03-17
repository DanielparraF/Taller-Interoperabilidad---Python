"""
Paso 6 — Segundo Proveedor Externo: PayFast

Interfaz completamente distinta a los proveedores anteriores:
  charge(account_ref, value, ref_code)
    → { ok, transaction_ref, error_msg }
"""

import random
import string


class ProveedorPayFast:
    """
    Segundo proveedor externo con API completamente diferente.
    Ni el nombre de métodos ni los campos tienen relación con V1 o V2.
    """

    def charge(self, account_ref: str, value: float, ref_code: str) -> dict:
        """
        Cobra un monto a una cuenta.

        Args:
            account_ref: Referencia de cuenta del cliente en PayFast.
            value:       Valor a cobrar.
            ref_code:    Código de referencia generado por el llamador.

        Returns:
            dict con: ok (bool), transaction_ref (str), error_msg (str|None)
        """
        transaction_ref = "PF-" + "".join(random.choices(string.digits, k=8))

        return {
            "ok":              True,
            "transaction_ref": transaction_ref,
            "error_msg":       None
        }
