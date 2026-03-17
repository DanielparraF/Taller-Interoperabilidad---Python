"""
Paso 3 — Sistema Principal desacoplado
 
Depende ÚNICAMENTE del contrato ServicioPago.
No conoce ningún proveedor externo.
"""
 
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 
from paso3_contrato.servicio_pago import ServicioPago, ResultadoPago
 
 
class SistemaPrincipal:
    """
    Sistema de órdenes desacoplado.
    Solo conoce el contrato ServicioPago — nunca los proveedores concretos.
    El proveedor se inyecta en el constructor (inyección de dependencia).
    """
 
    def __init__(self, servicio_pago: ServicioPago):
        self._pago = servicio_pago
 
    def crearOrden(self, cliente_id: str, monto: float) -> ResultadoPago:
        print(f"  [SistemaPrincipal] crearOrden(cliente_id='{cliente_id}', monto={monto})")
        print(f"  [SistemaPrincipal] → self._pago.procesarPago()  ← solo conoce el contrato")
 
        resultado = self._pago.procesarPago(cliente_id, monto)
 
        print(f"  [SistemaPrincipal] ← resultado: {resultado}")
        return resultado
 
 
if __name__ == "__main__":
    # Demostración rápida — requiere un adaptador concreto
    # Ejecutar desde la raíz del proyecto: python paso3_contrato/sistema_principal.py
    from paso4_adaptador.adaptador_v1 import AdaptadorProveedorV1
 
    print("=" * 55)
    print("  Paso 3 — Sistema principal desacoplado")
    print("=" * 55)
    cliente_id = input("  ID cliente : ").strip() or "cliente-001"
    monto      = float(input("  Monto      : ") or 150.00)
 
    sistema   = SistemaPrincipal(AdaptadorProveedorV1())
    resultado = sistema.crearOrden(cliente_id, monto)
    print(f"\n  Resultado: estado={resultado.estado}, autorizacion={resultado.codigo_autorizacion}")
