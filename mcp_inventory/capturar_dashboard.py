"""
Genera una imagen PNG del dashboard (sin necesitar navegador).
Jonathan Dario Sierra Galindo — Actividad 6
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.join(os.path.dirname(__file__), "capturas")
os.makedirs(OUT_DIR, exist_ok=True)

import csv
CARPETA = os.path.join(os.path.dirname(__file__), "data")

def leer_csv(nombre):
    ruta = os.path.join(CARPETA, nombre)
    if not os.path.exists(ruta): return []
    with open(ruta, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

inventario  = leer_csv("inventario.csv")
ventas_proc = leer_csv("ventas_procesadas.csv")
predicciones= leer_csv("predicciones.csv")

alertas = [p for p in inventario if int(p["cantidad"]) < int(p["stock_minimo"])]
top5    = sorted(ventas_proc, key=lambda x: int(x["total_unidades"]), reverse=True)[:5]
total_u = sum(int(v["total_unidades"]) for v in ventas_proc)
total_i = sum(float(v["total_ingresos"]) for v in ventas_proc)

# ─── Fuentes ──────────────────────────────────────────────────
def fuente(tam):
    for path in ["C:/Windows/Fonts/arialbd.ttf","C:/Windows/Fonts/arial.ttf","C:/Windows/Fonts/cour.ttf"]:
        try:
            return ImageFont.truetype(path, tam)
        except: pass
    return ImageFont.load_default()

FNT_TITLE = fuente(18)
FNT_H     = fuente(13)
FNT_BODY  = fuente(11)
FNT_VAL   = fuente(22)
FNT_LBL   = fuente(10)

# ─── Colores ──────────────────────────────────────────────────
FONDO   = (240, 242, 245)
AZUL    = (26, 58, 92)
AZUL_C  = (219, 233, 248)
BLANCO  = (255, 255, 255)
ROJO    = (220, 50, 50)
NARANJA = (220, 120, 10)
VERDE   = (30, 140, 60)
GRIS    = (170, 170, 170)
NEGRO   = (30, 30, 30)

W = 900
PAD = 20

# ─── Imagen ───────────────────────────────────────────────────
img = Image.new("RGB", (W, 720), FONDO)
d = ImageDraw.Draw(img)

# Header
d.rectangle([0, 0, W, 56], fill=AZUL)
d.text((PAD, 10), "Dashboard de Inventario — Sistema MCP", font=FNT_TITLE, fill=BLANCO)
d.text((PAD, 35), "Jonathan Dario Sierra Galindo | Computacion Cognitiva para Big Data", font=FNT_LBL, fill=(180,200,220))

# Tarjetas KPI
tarjetas = [
    (f"{total_u:,}",   "Unidades vendidas (90 dias)", AZUL),
    (f"${total_i/1_000_000:.1f}M", "Ingresos totales (COP)",    AZUL),
    (str(len(inventario)), "Productos en inventario",  AZUL),
    (str(len(alertas)),    "Alertas de stock bajo",    ROJO),
]
CARD_W = (W - PAD*2 - 12*3) // 4
cy = 70
for i, (val, lbl, color) in enumerate(tarjetas):
    cx = PAD + i * (CARD_W + 12)
    d.rectangle([cx, cy, cx+CARD_W, cy+72], fill=BLANCO, outline=(200,210,225))
    d.text((cx+12, cy+8),  val, font=FNT_VAL, fill=color)
    d.text((cx+12, cy+50), lbl, font=FNT_LBL, fill=GRIS)

# Sección Alertas
y = 158
d.rectangle([PAD, y, W-PAD, y+22], fill=AZUL)
d.text((PAD+8, y+4), "Alertas de Stock", font=FNT_H, fill=BLANCO)
y += 22
encabezados = ["Producto", "Cat.", "Stock", "Minimo", "Accion"]
anchos = [220, 110, 70, 70, 170]
xc = PAD
for enc, ancho in zip(encabezados, anchos):
    d.rectangle([xc, y, xc+ancho, y+20], fill=AZUL_C, outline=(200,210,225))
    d.text((xc+4, y+4), enc, font=FNT_LBL, fill=AZUL)
    xc += ancho
y += 20
for j, p in enumerate(alertas[:4]):
    cant = int(p["cantidad"]); minimo = int(p["stock_minimo"])
    color_fila = (255,245,245) if j%2==0 else BLANCO
    d.rectangle([PAD, y, W-PAD, y+20], fill=color_fila, outline=(220,220,220))
    xc = PAD
    datos = [p["nombre"], p["categoria"], str(cant), str(minimo), f"Reponer {minimo-cant} uds."]
    for dato, ancho in zip(datos, anchos):
        col = ROJO if dato.startswith("Repo") else NEGRO
        d.text((xc+4, y+4), dato, font=FNT_BODY, fill=col)
        xc += ancho
    y += 20

# Sección Top Ventas
y += 12
d.rectangle([PAD, y, W-PAD, y+22], fill=AZUL)
d.text((PAD+8, y+4), "Productos Mas Vendidos — Top 5 (90 dias)", font=FNT_H, fill=BLANCO)
y += 22
encabezados2 = ["Producto", "Unidades", "Ingresos (COP)", "Rotacion"]
anchos2 = [260, 100, 160, 120]
xc = PAD
for enc, ancho in zip(encabezados2, anchos2):
    d.rectangle([xc, y, xc+ancho, y+20], fill=AZUL_C, outline=(200,210,225))
    d.text((xc+4, y+4), enc, font=FNT_LBL, fill=AZUL)
    xc += ancho
y += 20
for j, v in enumerate(top5):
    color_fila = (245,248,255) if j%2==0 else BLANCO
    d.rectangle([PAD, y, W-PAD, y+20], fill=color_fila, outline=(220,220,220))
    xc = PAD
    datos = [v["nombre"], v["total_unidades"], f"${float(v['total_ingresos']):,.0f}", f"{v['promedio_semanal']} uds/sem"]
    for dato, ancho in zip(datos, anchos2):
        d.text((xc+4, y+4), str(dato), font=FNT_BODY, fill=NEGRO)
        xc += ancho
    y += 20

# Sección Predicciones
y += 12
d.rectangle([PAD, y, W-PAD, y+22], fill=AZUL)
d.text((PAD+8, y+4), "Prediccion de Demanda — Proxima Semana", font=FNT_H, fill=BLANCO)
y += 22
encabezados3 = ["Producto", "Demanda estimada (uds)", "Error MAE"]
anchos3 = [280, 200, 120]
xc = PAD
for enc, ancho in zip(encabezados3, anchos3):
    d.rectangle([xc, y, xc+ancho, y+20], fill=AZUL_C, outline=(200,210,225))
    d.text((xc+4, y+4), enc, font=FNT_LBL, fill=AZUL)
    xc += ancho
y += 20
for j, p in enumerate(predicciones[:5]):
    color_fila = (245,255,248) if j%2==0 else BLANCO
    d.rectangle([PAD, y, W-PAD, y+20], fill=color_fila, outline=(220,220,220))
    xc = PAD
    datos = [p["nombre"], p["demanda_estimada"], f"±{p['error_mae']}"]
    for dato, ancho in zip(datos, anchos3):
        d.text((xc+4, y+4), str(dato), font=FNT_BODY, fill=NEGRO)
        xc += ancho
    y += 20

# Footer
d.text((PAD, W-180), f"localhost:{5002} | Sistema MCP Inventario — Actividad 6", font=FNT_LBL, fill=GRIS)

salida = os.path.join(OUT_DIR, "cap10_dashboard.png")
img.save(salida)
print(f"Dashboard guardado: {salida}")
