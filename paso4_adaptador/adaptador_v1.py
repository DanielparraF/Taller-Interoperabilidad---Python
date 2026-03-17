"""
Paso 4 — Adaptador para ProveedorExternoV1

Traduce:
  procesarPago(cliente_id, monto)
    → executeTransaction(user, amount, currency)

Y convierte la respuesta:
  { resultCode, authId }
    → ResultadoPago(estado, codigo_autorizacion)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paso3_contrato.servicio_pago import ServicioPago, ResultadoPago
from paso1_acoplado.proveedor_externo_v1 import ProveedorExternoV1


class AdaptadorProveedorV1(ServicioPago):
    """
    Adapta ProveedorExternoV1 al contrato ServicioPago.
    El sistema principal NO conoce este archivo — solo conoce ServicioPago.
    """

    def __init__(self):
        self._proveedor = ProveedorExternoV1()

    def procesarPago(self, cliente_id: str, monto: float) -> ResultadoPago:
        print(f"  [AdaptadorV1] Traduciendo → procesarPago('{cliente_id}', {monto})"
              f" a executeTransaction(user, amount, currency)")

        # ── Traducción de parámetros internos → formato externo ──
        respuesta = self._proveedor.executeTransaction(
            user=cliente_id,    # cliente_id → user
            amount=monto,       # monto      → amount
            currency="USD"
        )

        # ── Traducción de respuesta externa → contrato interno ──
        estado = "APROBADO" if respuesta["resultCode"] == "00" else "RECHAZADO"

        return ResultadoPago(
            estado=estado,
            codigo_autorizacion=respuesta["authId"]   # authId → codigo_autorizacion
        )


if __name__ == "__main__":
    from paso3_contrato.sistema_principal import SistemaPrincipal

    print("=" * 55)
    print("  Paso 4 — Sistema con AdaptadorProveedorV1")
    print("=" * 55)
    cliente_id = input("  ID cliente : ").strip() or "cliente-001"
    monto      = float(input("  Monto      : ") or 250.00)

    sistema   = SistemaPrincipal(AdaptadorProveedorV1())
    resultado = sistema.crearOrden(cliente_id, monto)
    print(f"\n  Resultado: estado={resultado.estado}, autorizacion={resultado.codigo_autorizacion}")