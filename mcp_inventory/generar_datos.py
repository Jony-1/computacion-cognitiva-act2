"""
Genera datos simulados de inventario y ventas en archivos CSV.
Jonathan Dario Sierra Galindo — Actividad 6
"""
import csv
import random
import os
from datetime import date, timedelta

# Directorio de datos
CARPETA = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(CARPETA, exist_ok=True)

random.seed(42)

# ─── Productos base ───────────────────────────────────────────
productos_base = [
    {"id": 1, "nombre": "Laptop HP 14",        "categoria": "Electronica",  "precio": 2_350_000, "stock_minimo": 3},
    {"id": 2, "nombre": "Monitor Samsung 24",  "categoria": "Electronica",  "precio": 1_200_000, "stock_minimo": 2},
    {"id": 3, "nombre": "Silla Ergonomica",    "categoria": "Mobiliario",   "precio":   850_000, "stock_minimo": 5},
    {"id": 4, "nombre": "Teclado Mecanico",    "categoria": "Accesorios",   "precio":   320_000, "stock_minimo": 10},
    {"id": 5, "nombre": "Mouse Inalambrico",   "categoria": "Accesorios",   "precio":   150_000, "stock_minimo": 10},
    {"id": 6, "nombre": "Cable HDMI 2m",       "categoria": "Cables",       "precio":    35_000, "stock_minimo": 20},
    {"id": 7, "nombre": "Disco SSD 500GB",     "categoria": "Almacenamiento","precio":  450_000, "stock_minimo": 5},
    {"id": 8, "nombre": "Webcam Full HD",      "categoria": "Accesorios",   "precio":   280_000, "stock_minimo": 4},
]

# ─── inventario.csv ───────────────────────────────────────────
ruta_inv = os.path.join(CARPETA, "inventario.csv")
with open(ruta_inv, "w", newline="", encoding="utf-8") as f:
    campos = ["id", "nombre", "categoria", "precio", "cantidad", "stock_minimo"]
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader()
    for p in productos_base:
        cantidad = random.randint(0, 30)
        w.writerow({
            "id": p["id"],
            "nombre": p["nombre"],
            "categoria": p["categoria"],
            "precio": p["precio"],
            "cantidad": cantidad,
            "stock_minimo": p["stock_minimo"],
        })
print(f"Creado: {ruta_inv}")

# ─── productos.csv ────────────────────────────────────────────
ruta_prod = os.path.join(CARPETA, "productos.csv")
with open(ruta_prod, "w", newline="", encoding="utf-8") as f:
    campos = ["id", "nombre", "categoria", "precio"]
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader()
    for p in productos_base:
        w.writerow({"id": p["id"], "nombre": p["nombre"],
                    "categoria": p["categoria"], "precio": p["precio"]})
print(f"Creado: {ruta_prod}")

# ─── ventas.csv — 90 dias de historial ───────────────────────
ruta_ventas = os.path.join(CARPETA, "ventas.csv")
hoy = date(2026, 6, 7)
venta_id = 1
with open(ruta_ventas, "w", newline="", encoding="utf-8") as f:
    campos = ["venta_id", "producto_id", "nombre", "fecha", "cantidad_vendida", "precio_unitario", "total"]
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader()
    for dias_atras in range(90, 0, -1):
        fecha = hoy - timedelta(days=dias_atras)
        # Entre 2 y 6 ventas por dia
        num_ventas = random.randint(2, 6)
        productos_dia = random.choices(productos_base, k=num_ventas)
        for p in productos_dia:
            cant = random.randint(1, 5)
            w.writerow({
                "venta_id": venta_id,
                "producto_id": p["id"],
                "nombre": p["nombre"],
                "fecha": fecha.isoformat(),
                "cantidad_vendida": cant,
                "precio_unitario": p["precio"],
                "total": cant * p["precio"],
            })
            venta_id += 1
print(f"Creado: {ruta_ventas} ({venta_id-1} registros de ventas)")
print("\nDatos simulados generados en:", CARPETA)
