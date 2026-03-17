"""
Paso 4 — Adaptador para ProveedorExternoV2

El proveedor cambió su interfaz. El sistema principal NO se modifica.
Solo se actualiza este adaptador.

Traduce:
  procesarPago(cliente_id, monto)
    → processPayment(customerId, totalAmount, currencyCode)

Y convierte la respuesta:
  { status, confirmationCode }
    → ResultadoPago(estado, codigo_autorizacion)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paso3_contrato.servicio_pago import ServicioPago, ResultadoPago
from paso2_impacto.proveedor_externo_v2 import ProveedorExternoV2


class AdaptadorProveedorV2(ServicioPago):
    """
    Adapta ProveedorExternoV2 (interfaz cambiada) al contrato ServicioPago.
    El sistema principal no cambia — solo este adaptador se actualiza.
    """

    def __init__(self):
        self._proveedor = ProveedorExternoV2()

    def procesarPago(self, cliente_id: str, monto: float) -> ResultadoPago:
        print(f"  [AdaptadorV2] Traduciendo → procesarPago('{cliente_id}', {monto})"
              f" a processPayment(customerId, totalAmount, currencyCode)")

        # ── Traducción de parámetros internos → formato externo ──
        respuesta = self._proveedor.processPayment(
            customerId=cliente_id,    # cliente_id → customerId
            totalAmount=monto,        # monto      → totalAmount
            currencyCode="USD"
        )

        # ── Traducción de respuesta externa → contrato interno ──
        estado = "APROBADO" if respuesta["status"] == "SUCCESS" else "RECHAZADO"

        return ResultadoPago(
            estado=estado,
            codigo_autorizacion=respuesta["confirmationCode"]  # confirmationCode → codigo_autorizacion
        )


if __name__ == "__main__":
    from paso3_contrato.sistema_principal import SistemaPrincipal

    print("=" * 55)
    print("  Paso 4 — Sistema con AdaptadorProveedorV2 (interfaz cambiada)")
    print("  El sistema principal NO se modifico")
    print("=" * 55)
    cliente_id = input("  ID cliente : ").strip() or "cliente-001"
    monto      = float(input("  Monto      : ") or 250.00)

    sistema   = SistemaPrincipal(AdaptadorProveedorV2())
    resultado = sistema.crearOrden(cliente_id, monto)
    print(f"\n  Resultado: estado={resultado.estado}, autorizacion={resultado.codigo_autorizacion}")