"""
Modelo de prediccion de demanda usando regresion lineal.
Predice cuantas unidades se venderan la proxima semana por producto.
Jonathan Dario Sierra Galindo — Actividad 6
"""
import csv
import os
from collections import defaultdict

CARPETA = os.path.join(os.path.dirname(__file__), "data")

# ─── Cargar historial de ventas ───────────────────────────────
ruta_ventas = os.path.join(CARPETA, "ventas.csv")
ventas_semana = defaultdict(lambda: defaultdict(int))  # {producto_id: {semana: cant}}
nombres = {}

with open(ruta_ventas, "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    for fila in lector:
        pid = fila["producto_id"]
        nombres[pid] = fila["nombre"]
        from datetime import date
        anio, mes, dia = map(int, fila["fecha"].split("-"))
        semana = date(anio, mes, dia).isocalendar()[1]
        ventas_semana[pid][semana] += int(fila["cantidad_vendida"])

# ─── Regresion lineal simple (sin scikit-learn) ───────────────
def regresion_lineal(xs, ys):
    """Calcula pendiente e intercepto de y = m*x + b."""
    n = len(xs)
    if n < 2:
        return 0, sum(ys) / n if n else 0
    suma_x  = sum(xs)
    suma_y  = sum(ys)
    suma_xy = sum(x * y for x, y in zip(xs, ys))
    suma_xx = sum(x * x for x in xs)
    denominador = n * suma_xx - suma_x ** 2
    if denominador == 0:
        return 0, suma_y / n
    m = (n * suma_xy - suma_x * suma_y) / denominador
    b = (suma_y - m * suma_x) / n
    return m, b

def error_mae(ys_real, ys_pred):
    """Error absoluto medio."""
    return sum(abs(r - p) for r, p in zip(ys_real, ys_pred)) / len(ys_real)

# ─── Prediccion para cada producto ───────────────────────────
print(f"{'Producto':<25} {'Demanda estimada':>17} {'Error (MAE)':>12}")
print("-" * 56)

proxima_semana = max(
    max(s for s in semanas.keys())
    for semanas in ventas_semana.values()
) + 1

predicciones = []
for pid, semanas in sorted(ventas_semana.items(), key=lambda x: x[0]):
    xs = sorted(semanas.keys())
    ys = [semanas[s] for s in xs]

    m, b = regresion_lineal(xs, ys)
    demanda = max(0, round(m * proxima_semana + b, 1))

    ys_pred = [m * x + b for x in xs]
    mae = round(error_mae(ys, ys_pred), 2)

    nombre = nombres.get(pid, f"Producto {pid}")
    print(f"{nombre:<25} {demanda:>17.1f} {mae:>+12.2f}")

    predicciones.append({
        "producto_id":    pid,
        "nombre":         nombre,
        "demanda_estimada": demanda,
        "error_mae":      mae,
    })

# ─── Guardar predicciones ─────────────────────────────────────
ruta_pred = os.path.join(CARPETA, "predicciones.csv")
with open(ruta_pred, "w", newline="", encoding="utf-8") as f:
    campos = ["producto_id", "nombre", "demanda_estimada", "error_mae"]
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader()
    w.writerows(predicciones)

print(f"\nPredicciones guardadas en: {ruta_pred}")
