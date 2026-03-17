"""
Paso 1 — Implementación ingenua (acoplada)

El sistema principal llama DIRECTAMENTE al proveedor externo.
Nivel de acoplamiento: ALTO

Puntos de acoplamiento:
  1. Nombre del método:      executeTransaction()
  2. Parámetro:              user=
  3. Parámetro:              amount=
  4. Clave de respuesta:     respuesta["resultCode"]
  5. Clave de respuesta:     respuesta["authId"]
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paso1_acoplado.proveedor_externo_v1 import ProveedorExternoV1


class SistemaPrincipalAcoplado:
    """
    Sistema de órdenes ACOPLADO directamente al proveedor externo.
    Cualquier cambio en el proveedor rompe esta clase.
    """

    def __init__(self):
        self.proveedor = ProveedorExternoV1()          # ← acoplamiento directo

    def crearOrden(self, cliente_id: str, monto: float) -> dict:
        print(f"  [SistemaPrincipalAcoplado] crearOrden('{cliente_id}', {monto})")

        respuesta = self.proveedor.executeTransaction(  # ← acoplado al método
            user=cliente_id,                            # ← acoplado al parámetro
            amount=monto,                               # ← acoplado al parámetro
            currency="USD"
        )

        if respuesta["resultCode"] == "00":             # ← acoplado a la clave
            return {
                "estado": "APROBADO",
                "codigoAutorizacion": respuesta["authId"]  # ← acoplado a la clave
            }
        return {"estado": "RECHAZADO", "codigoAutorizacion": None}


if __name__ == "__main__":
    print("=" * 55)
    print("  Paso 1 — Sistema acoplado directamente al proveedor")
    print("=" * 55)
    cliente_id = input("  ID cliente : ").strip() or "cliente-001"
    monto      = float(input("  Monto      : ") or 150.00)

    sistema   = SistemaPrincipalAcoplado()
    resultado = sistema.crearOrden(cliente_id, monto)
    print(f"\n  Resultado: {resultado}")