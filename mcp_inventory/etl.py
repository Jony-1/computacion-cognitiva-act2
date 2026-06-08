"""
Proceso ETL: extrae ventas.csv, transforma y carga ventas_procesadas.csv
Jonathan Dario Sierra Galindo — Actividad 6
"""
import csv
import os
from collections import defaultdict

CARPETA = os.path.join(os.path.dirname(__file__), "data")

# ─── EXTRAER ──────────────────────────────────────────────────
ruta_ventas = os.path.join(CARPETA, "ventas.csv")
registros = []
with open(ruta_ventas, "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    for fila in lector:
        registros.append(fila)

print(f"[ETL] Registros extraidos: {len(registros)}")

# ─── TRANSFORMAR ──────────────────────────────────────────────
# Agrupar ventas por producto y semana
ventas_por_producto = defaultdict(list)
for r in registros:
    pid = r["producto_id"]
    cant = int(r["cantidad_vendida"])
    fecha = r["fecha"]
    # Semana del año a partir de la fecha
    anio, mes, dia = map(int, fecha.split("-"))
    from datetime import date
    semana = date(anio, mes, dia).isocalendar()[1]
    ventas_por_producto[pid].append({
        "nombre": r["nombre"],
        "semana": semana,
        "cantidad_vendida": cant,
        "total": float(r["total"]),
    })

# Calcular totales y promedios por producto
resumen = []
for pid, ventas in ventas_por_producto.items():
    nombre = ventas[0]["nombre"]
    total_unidades = sum(v["cantidad_vendida"] for v in ventas)
    total_ingresos = sum(v["total"] for v in ventas)
    semanas_unicas = len(set(v["semana"] for v in ventas))
    promedio_semanal = round(total_unidades / semanas_unicas, 2) if semanas_unicas > 0 else 0

    resumen.append({
        "producto_id":       pid,
        "nombre":            nombre,
        "total_unidades":    total_unidades,
        "total_ingresos":    total_ingresos,
        "semanas_activas":   semanas_unicas,
        "promedio_semanal":  promedio_semanal,
    })

print(f"[ETL] Productos procesados: {len(resumen)}")

# ─── CARGAR ───────────────────────────────────────────────────
ruta_salida = os.path.join(CARPETA, "ventas_procesadas.csv")
campos = ["producto_id", "nombre", "total_unidades", "total_ingresos",
          "semanas_activas", "promedio_semanal"]

with open(ruta_salida, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader()
    for fila in resumen:
        w.writerow(fila)

print(f"[ETL] Archivo generado: {ruta_salida}")
print("[ETL] Proceso ETL completado exitosamente.")
