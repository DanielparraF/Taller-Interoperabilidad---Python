"""
Paso 2 — Análisis de impacto del cambio

Demuestra que el sistema acoplado se rompe cuando el proveedor
cambia su interfaz, sin que el sistema principal haya cambiado.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from paso2_impacto.proveedor_externo_v2 import ProveedorExternoV2


class SistemaPrincipalRoto:
    """
    El mismo sistema acoplado del Paso 1, pero ahora apuntando a V2.
    Se rompe porque llama a executeTransaction() que ya no existe.
    """

    def __init__(self):
        self.proveedor = ProveedorExternoV2()   # ← mismo patrón, proveedor cambiado

    def crearOrden(self, cliente_id: str, monto: float) -> dict:
        # ← ROTO: executeTransaction ya no existe en V2
        respuesta = self.proveedor.executeTransaction(   # type: ignore
            user=cliente_id,
            amount=monto,
            currency="USD"
        )
        if respuesta["resultCode"] == "00":             # type: ignore
            return {
                "estado": "APROBADO",
                "codigoAutorizacion": respuesta["authId"]  # type: ignore
            }
        return {"estado": "RECHAZADO", "codigoAutorizacion": None}


if __name__ == "__main__":
    print("=" * 55)
    print("  Paso 2 — Demostración de rotura por cambio de proveedor")
    print("=" * 55)

    sistema = SistemaPrincipalRoto()
    try:
        resultado = sistema.crearOrden("cliente-001", 200.00)
        print(f"  Resultado: {resultado}")
    except AttributeError as e:
        print(f"\n  ERROR: {type(e).__name__}: {e}")
        print("\n  Líneas que requieren modificación en el sistema principal:")
        roturas = [
            "executeTransaction()  →  ahora es processPayment()",
            "user=              →  ahora es customerId=",
            "amount=            →  ahora es totalAmount=",
            'resultCode         →  ahora es status ("SUCCESS")',
            "authId             →  ahora es confirmationCode",
        ]
        for r in roturas:
            print(f"    ✗ {r}")
