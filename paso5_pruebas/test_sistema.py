"""
Paso 5 — Pruebas automatizadas

Verifica que el sistema principal continúa funcionando cuando el proveedor
cambia, siempre que el adaptador se actualice correctamente.
"""

import sys, os, unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from paso3_contrato.servicio_pago    import ServicioPago, ResultadoPago
from paso3_contrato.sistema_principal import SistemaPrincipal
from paso4_adaptador.adaptador_v1    import AdaptadorProveedorV1
from paso4_adaptador.adaptador_v2    import AdaptadorProveedorV2
from paso6_segundo_proveedor.adaptador_payfast import AdaptadorPayFast


# ── Stubs mínimos del contrato ────────────────────────────────────────────────

class ServicioPagoAprobado(ServicioPago):
    def procesarPago(self, cliente_id, monto):
        return ResultadoPago(estado="APROBADO", codigo_autorizacion="AUTH-TEST")

class ServicioPagoRechazado(ServicioPago):
    def procesarPago(self, cliente_id, monto):
        return ResultadoPago(estado="RECHAZADO", codigo_autorizacion="RECHAZADO")


# ── Suite ─────────────────────────────────────────────────────────────────────

class TestSistemaPrincipalAisladoDelProveedor(unittest.TestCase):
    """El sistema principal NO se modifica entre ninguna de estas pruebas."""

    def test_orden_aprobada_con_stub(self):
        sistema = SistemaPrincipal(ServicioPagoAprobado())
        r = sistema.crearOrden("c-001", 100)
        self.assertEqual(r.estado, "APROBADO")
        self.assertIsNotNone(r.codigo_autorizacion)

    def test_orden_rechazada_con_stub(self):
        sistema = SistemaPrincipal(ServicioPagoRechazado())
        r = sistema.crearOrden("c-002", 50)
        self.assertEqual(r.estado, "RECHAZADO")

    def test_sistema_funciona_con_proveedor_v1(self):
        sistema = SistemaPrincipal(AdaptadorProveedorV1())
        r = sistema.crearOrden("c-001", 200)
        self.assertEqual(r.estado, "APROBADO")
        self.assertEqual(r.codigo_autorizacion, "AUTH-9821")

    def test_sistema_funciona_con_proveedor_v2_sin_cambiar_sistema(self):
        """PRUEBA CLAVE: proveedor cambió — sistema principal intacto."""
        sistema = SistemaPrincipal(AdaptadorProveedorV2())
        r = sistema.crearOrden("c-001", 200)
        self.assertEqual(r.estado, "APROBADO")
        self.assertEqual(r.codigo_autorizacion, "CONF-7734")

    def test_sistema_funciona_con_payfast(self):
        """Paso 6: segundo proveedor — sistema principal intacto."""
        sistema = SistemaPrincipal(AdaptadorPayFast())
        r = sistema.crearOrden("c-003", 320000)
        self.assertEqual(r.estado, "APROBADO")
        self.assertTrue(r.codigo_autorizacion.startswith("PF-"))

    def test_contrato_siempre_devuelve_resultado_pago(self):
        """El contrato garantiza que siempre se devuelve un ResultadoPago."""
        for adaptador in [AdaptadorProveedorV1(), AdaptadorProveedorV2(), AdaptadorPayFast()]:
            sistema = SistemaPrincipal(adaptador)
            r = sistema.crearOrden("c-test", 10)
            self.assertIsInstance(r, ResultadoPago)
            self.assertIn(r.estado, ["APROBADO", "RECHAZADO"])

    def test_sistema_solo_llama_procesarPago(self):
        """El sistema principal SOLO invoca procesarPago — nunca métodos del proveedor."""
        mock = MagicMock(spec=ServicioPago)
        mock.procesarPago.return_value = ResultadoPago("APROBADO", "MOCK-001")
        sistema = SistemaPrincipal(mock)
        sistema.crearOrden("c-mock", 75)
        mock.procesarPago.assert_called_once_with("c-mock", 75)


if __name__ == "__main__":
    unittest.main(verbosity=2)
