# Taller Adaptador de Interfaz

## 📌 Descripción

Este proyecto corresponde al taller de **Interoperabilidad usando el patrón Adaptador** en la materia Ingeniería de Software II.

El objetivo es simular un sistema de órdenes que necesita procesar pagos mediante un proveedor externo, el cual puede cambiar su estructura sin previo aviso.

Para solucionar este problema se implementa un **adaptador**, que permite desacoplar el sistema principal del proveedor.

---

## 🎯 Objetivo

Implementar una estrategia de interoperabilidad que permita:

* Reducir el acoplamiento
* Mantener un contrato interno estable
* Soportar cambios en proveedores externos sin afectar el sistema principal

---

## ⚙️ Estructura del proyecto

El proyecto está dividido en varias partes:

* `sistema_principal/` → lógica principal del sistema
* `proveedor_externo_v1/` → primera versión del proveedor
* `proveedor_externo_v2/` → proveedor modificado (simula cambios)
* `adaptadores/` → contiene los adaptadores
* `tests/` → pruebas del sistema

---

## 🔴 Implementación inicial (acoplada)

En la primera parte, el sistema se conecta directamente con el proveedor externo.

Problemas:

* Alto acoplamiento
* Dependencia directa de nombres y estructura
* Si el proveedor cambia, el sistema falla

---

## 🟡 Uso del Adaptador

Se define una interfaz interna:

```
procesarPago(clienteId, monto)
```

Luego se crean adaptadores que:

* Traducen los parámetros
* Transforman la respuesta
* Ocultan la lógica del proveedor

Esto permite que el sistema principal no dependa del proveedor directamente.

---

## 🟢 Pruebas

Se implementa una prueba automatizada que verifica que:

* El sistema sigue funcionando
* Aunque el proveedor cambie
* Siempre que el adaptador se actualice

---

## 🔵 Segundo proveedor

Se agrega un segundo proveedor con una interfaz distinta.

Resultado:

* El sistema funciona sin cambios
* Solo se crea un nuevo adaptador

---



## 💡 Conclusiones

* El patrón Adaptador reduce el acoplamiento
* Mejora la mantenibilidad del sistema
* Permite integrar múltiples proveedores
* Aunque agrega algo de complejidad, es útil en sistemas reales

---

## 🚀 Cómo ejecutar

1. Clonar el repositorio
2. Ejecutar el sistema principal
3. Ejecutar las pruebas

Ejemplo:

```
python sistema_principal.py
python test_sistema.py
```

---

## 👨‍💻 Autor

Daniel Esteban Parra Flechas 
Manuel Felipe Pineda Abril
Estudiante de Ingeniería de Sistemas
Universidad Pedagógica y tecnológica de Colombia 
