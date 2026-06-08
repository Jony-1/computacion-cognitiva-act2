"""
Dashboard Flask para el sistema de inventario — Puerto 5002
Muestra: unidades vendidas, productos mas vendidos, rotacion, alertas de stock.
Jonathan Dario Sierra Galindo — Actividad 6
"""
import csv
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

CARPETA = os.path.join(os.path.dirname(__file__), "data")
PUERTO = 5002

# ─── Leer datos ──────────────────────────────────────────────

def leer_csv(nombre):
    ruta = os.path.join(CARPETA, nombre)
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

# ─── Construir HTML ──────────────────────────────────────────

def construir_html():
    inventario = leer_csv("inventario.csv")
    ventas_proc = leer_csv("ventas_procesadas.csv")
    predicciones = leer_csv("predicciones.csv")

    # Alertas de stock: cantidad < stock_minimo
    alertas = [
        p for p in inventario
        if int(p["cantidad"]) < int(p["stock_minimo"])
    ]

    # Productos mas vendidos (top 5)
    ventas_ord = sorted(ventas_proc, key=lambda x: int(x["total_unidades"]), reverse=True)[:5]

    # Total unidades vendidas
    total_unidades = sum(int(v["total_unidades"]) for v in ventas_proc)
    total_ingresos = sum(float(v["total_ingresos"]) for v in ventas_proc)

    # ── Filas de tabla alertas ────────────────────────────────
    filas_alertas = ""
    for p in alertas:
        cant  = int(p["cantidad"])
        minimo = int(p["stock_minimo"])
        faltante = minimo - cant
        color = "#ff4444" if cant == 0 else "#ff8800"
        filas_alertas += f"""
        <tr>
          <td>{p['nombre']}</td>
          <td>{p['categoria']}</td>
          <td style="color:{color};font-weight:bold">{cant}</td>
          <td>{minimo}</td>
          <td style="color:{color};font-weight:bold">Reponer {faltante} uds.</td>
        </tr>"""

    if not filas_alertas:
        filas_alertas = '<tr><td colspan="5" style="color:green;text-align:center">Sin alertas — stock en orden</td></tr>'

    # ── Filas top ventas ──────────────────────────────────────
    filas_ventas = ""
    for v in ventas_ord:
        filas_ventas += f"""
        <tr>
          <td>{v['nombre']}</td>
          <td>{v['total_unidades']}</td>
          <td>${float(v['total_ingresos']):,.0f}</td>
          <td>{v['promedio_semanal']} uds/sem</td>
        </tr>"""

    # ── Filas predicciones ────────────────────────────────────
    filas_pred = ""
    for p in predicciones:
        filas_pred += f"""
        <tr>
          <td>{p['nombre']}</td>
          <td>{p['demanda_estimada']}</td>
          <td>±{p['error_mae']}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Dashboard Inventario — MCP</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: Arial, sans-serif; background: #f0f2f5; color: #222; }}
    header {{ background: #1a3a5c; color: white; padding: 18px 30px; }}
    header h1 {{ font-size: 1.4rem; }}
    header p  {{ font-size: 0.85rem; opacity: 0.8; margin-top: 4px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr));
             gap: 16px; padding: 20px 30px 0; }}
    .card {{ background: white; border-radius: 8px; padding: 20px;
             box-shadow: 0 1px 4px rgba(0,0,0,.1); }}
    .card .val {{ font-size: 2rem; font-weight: bold; color: #1a3a5c; }}
    .card .lbl {{ font-size: 0.8rem; color: #777; margin-top: 4px; }}
    .alerta-card .val {{ color: #ff4444; }}
    section {{ margin: 20px 30px; background: white; border-radius: 8px;
               padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,.1); }}
    section h2 {{ font-size: 1rem; color: #1a3a5c; margin-bottom: 12px;
                  border-bottom: 2px solid #dbe9f8; padding-bottom: 6px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
    th {{ background: #1a3a5c; color: white; padding: 8px 10px; text-align: left; }}
    td {{ padding: 7px 10px; border-bottom: 1px solid #eee; }}
    tr:hover td {{ background: #f5f8ff; }}
    footer {{ text-align: center; padding: 16px; color: #aaa; font-size: 0.78rem; }}
  </style>
</head>
<body>
  <header>
    <h1>Dashboard de Inventario — Sistema MCP</h1>
    <p>Jonathan Dario Sierra Galindo | Computacion Cognitiva para Big Data</p>
  </header>

  <div class="grid">
    <div class="card">
      <div class="val">{total_unidades:,}</div>
      <div class="lbl">Unidades vendidas (90 dias)</div>
    </div>
    <div class="card">
      <div class="val">${total_ingresos:,.0f}</div>
      <div class="lbl">Ingresos totales (COP)</div>
    </div>
    <div class="card">
      <div class="val">{len(inventario)}</div>
      <div class="lbl">Productos en inventario</div>
    </div>
    <div class="card alerta-card">
      <div class="val">{len(alertas)}</div>
      <div class="lbl">Alertas de stock bajo</div>
    </div>
  </div>

  <section>
    <h2>Alertas de Stock</h2>
    <table>
      <tr><th>Producto</th><th>Categoria</th><th>Stock actual</th>
          <th>Stock minimo</th><th>Accion recomendada</th></tr>
      {filas_alertas}
    </table>
  </section>

  <section>
    <h2>Productos Mas Vendidos (Top 5 — 90 dias)</h2>
    <table>
      <tr><th>Producto</th><th>Unidades</th><th>Ingresos</th><th>Rotacion</th></tr>
      {filas_ventas}
    </table>
  </section>

  <section>
    <h2>Prediccion de Demanda — Proxima Semana (Regresion Lineal)</h2>
    <table>
      <tr><th>Producto</th><th>Demanda estimada (uds)</th><th>Error MAE</th></tr>
      {filas_pred}
    </table>
  </section>

  <footer>Sistema MCP Inventario — Actividad 6 | Puerto {PUERTO}</footer>
</body>
</html>"""


# ─── Servidor HTTP simple ─────────────────────────────────────

class ManejadorHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        contenido = construir_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def log_message(self, fmt, *args):
        print(f"[Dashboard] {self.address_string()} - {fmt % args}")


if __name__ == "__main__":
    servidor = HTTPServer(("localhost", PUERTO), ManejadorHTTP)
    print(f"Dashboard corriendo en http://localhost:{PUERTO}")
    print("Presiona Ctrl+C para detener.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
