"""
Script de prueba de las 9 operaciones del servidor MCP de inventario.
Ejecuta cada herramienta directamente e imprime resultados.
Jonathan Dario Sierra Galindo — Actividad 6
"""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))

# Borrar BD anterior para empezar limpio
if os.path.exists("inventario.db"):
    os.remove("inventario.db")

# Importar funciones del servidor directamente
from database import inicializar_bd, NOMBRE_BD
from server import (
    crear_producto,
    consultar_producto,
    actualizar_producto,
    eliminar_producto,
    listar_productos,
    calcular_valor_total_inventario,
    productos_agotados,
    producto_mas_costoso,
    estadisticas_inventario,
)

SEP = "=" * 60

print(SEP)
print("PRUEBA 1 — crear_producto")
print(SEP)
r1 = crear_producto("Laptop HP 14", "Electronica", 10, 2_500_000)
r2 = crear_producto("Monitor Samsung 24", "Electronica", 5, 1_200_000)
r3 = crear_producto("Silla Ergonomica", "Mobiliario", 0, 850_000)
r4 = crear_producto("Teclado Mecanico", "Accesorios", 20, 320_000)
r5 = crear_producto("Mouse Inalambrico", "Accesorios", 15, 150_000)
print(r1)
print(r2)
print(r3)
print(r4)
print(r5)

print()
print(SEP)
print("PRUEBA 2 — consultar_producto (ID=1)")
print(SEP)
print(consultar_producto(1))

print()
print(SEP)
print("PRUEBA 3 — actualizar_producto (ID=1)")
print(SEP)
print(actualizar_producto(1, cantidad=8, precio=2_350_000))

print()
print(SEP)
print("PRUEBA 4 — listar_productos")
print(SEP)
for p in listar_productos():
    print(p)

print()
print(SEP)
print("PRUEBA 5 — calcular_valor_total_inventario")
print(SEP)
print(calcular_valor_total_inventario())

print()
print(SEP)
print("PRUEBA 6 — productos_agotados")
print(SEP)
agotados = productos_agotados()
if agotados:
    for p in agotados:
        print(p)
else:
    print("(ningun producto agotado)")

print()
print(SEP)
print("PRUEBA 7 — producto_mas_costoso")
print(SEP)
print(producto_mas_costoso())

print()
print(SEP)
print("PRUEBA 8 — estadisticas_inventario")
print(SEP)
print(estadisticas_inventario())

print()
print(SEP)
print("PRUEBA 9 — eliminar_producto (ID=2)")
print(SEP)
print(eliminar_producto(2))
print("Lista final:")
for p in listar_productos():
    print(p)

print()
print(SEP)
print("Todas las pruebas completadas exitosamente.")
print(SEP)
