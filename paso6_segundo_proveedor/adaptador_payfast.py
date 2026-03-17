"""
Paso 6 — Adaptador para PayFast

Demuestra que el sistema principal puede usar un segundo proveedor
completamente diferente sin ninguna modificación.

Traduce:
  procesarPago(cliente_id, monto)
    → charge(account_ref, value, ref_code)

Y convierte la respuesta:
  { ok, transaction_ref, error_msg }
    → ResultadoPago(estado, codigo_autorizacion)
"""

import sys, os, uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paso3_contrato.servicio_pago import ServicioPago, ResultadoPago
from paso6_segundo_proveedor.proveedor_payfast import ProveedorPayFast


class AdaptadorPayFast(ServicioPago):
    """
    Adapta ProveedorPayFast al contrato ServicioPago.
    El sistema principal NO se modifica en ninguna línea.
    """

    def __init__(self):
        self._proveedor = ProveedorPayFast()

    def procesarPago(self, cliente_id: str, monto: float) -> ResultadoPago:
        ref_code = str(uuid.uuid4())[:8].upper()

        print(f"  [AdaptadorPayFast] Traduciendo → procesarPago('{cliente_id}', {monto})"
              f" a charge(account_ref, value, ref_code)")

        # ── Traducción de parámetros ──
        respuesta = self._proveedor.charge(
            account_ref=cliente_id,   # cliente_id → account_ref
            value=monto,              # monto      → value
            ref_code=ref_code         # generado localmente
        )

        # ── Traducción de respuesta ──
        estado = "APROBADO" if respuesta["ok"] else "RECHAZADO"

        return ResultadoPago(
            estado=estado,
            codigo_autorizacion=respuesta["transaction_ref"]  # transaction_ref → codigo_autorizacion
        )


if __name__ == "__main__":
    from paso3_contrato.sistema_principal import SistemaPrincipal

    print("=" * 55)
    print("  Paso 6 — Sistema con AdaptadorPayFast (segundo proveedor)")
    print("  El sistema principal NO se modifico")
    print("=" * 55)
    cliente_id = input("  ID cliente : ").strip() or "cliente-002"
    monto      = float(input("  Monto      : ") or 320000.00)

    sistema   = SistemaPrincipal(AdaptadorPayFast())
    resultado = sistema.crearOrden(cliente_id, monto)
    print(f"\n  Resultado: estado={resultado.estado}, autorizacion={resultado.codigo_autorizacion}")