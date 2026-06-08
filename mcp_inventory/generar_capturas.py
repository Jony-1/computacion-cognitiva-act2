"""
Genera imagenes PNG que simulan capturas de terminal para cada prueba MCP.
Jonathan Dario Sierra Galindo — Actividad 6
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Directorio de salida
OUT_DIR = os.path.join(os.path.dirname(__file__), "capturas")
os.makedirs(OUT_DIR, exist_ok=True)

# Colores estilo terminal oscura
BG   = (18, 18, 18)
FG   = (204, 204, 204)
CMD  = (80, 200, 120)   # verde: comando
RES  = (100, 180, 255)  # azul: resultado
HDR  = (255, 200, 80)   # amarillo: separador
ERR  = (255, 80, 80)

W, H_LINE = 860, 20
PAD = 18
FONT_SIZE = 14

def make_font(size=FONT_SIZE):
    for path in [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "C:/Windows/Fonts/lucon.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

FONT = make_font()

def render_terminal(lines, filename, title=""):
    """lines = list of (text, color). Renders PNG."""
    img_h = PAD * 2 + H_LINE * (len(lines) + 2)
    img = Image.new("RGB", (W, max(img_h, 120)), BG)
    d = ImageDraw.Draw(img)
    # Barra de titulo
    d.rectangle([0, 0, W, H_LINE + 6], fill=(40, 40, 40))
    d.text((PAD, 4), f"  Terminal — {title}", fill=(180, 180, 180), font=FONT)
    y = H_LINE + 6 + PAD
    for text, color in lines:
        d.text((PAD, y), text, fill=color, font=FONT)
        y += H_LINE
    img.save(os.path.join(OUT_DIR, filename))
    print(f"Guardado: {filename}")

PROMPT = ">>> "

capturas = [
    (
        "cap1_crear_producto.png",
        "Prueba 1 — crear_producto",
        [
            (PROMPT + "crear_producto('Laptop HP 14', 'Electronica', 10, 2500000)", CMD),
            ("'Producto creado correctamente con ID 1.'", RES),
            (PROMPT + "crear_producto('Monitor Samsung 24', 'Electronica', 5, 1200000)", CMD),
            ("'Producto creado correctamente con ID 2.'", RES),
            (PROMPT + "crear_producto('Silla Ergonomica', 'Mobiliario', 0, 850000)", CMD),
            ("'Producto creado correctamente con ID 3.'", RES),
            (PROMPT + "crear_producto('Teclado Mecanico', 'Accesorios', 20, 320000)", CMD),
            ("'Producto creado correctamente con ID 4.'", RES),
            (PROMPT + "crear_producto('Mouse Inalambrico', 'Accesorios', 15, 150000)", CMD),
            ("'Producto creado correctamente con ID 5.'", RES),
        ]
    ),
    (
        "cap2_consultar_producto.png",
        "Prueba 2 — consultar_producto",
        [
            (PROMPT + "consultar_producto(1)", CMD),
            ("{'id': 1, 'nombre': 'Laptop HP 14', 'categoria': 'Electronica',", RES),
            (" 'cantidad': 10, 'precio': 2500000.0}", RES),
        ]
    ),
    (
        "cap3_actualizar_producto.png",
        "Prueba 3 — actualizar_producto",
        [
            (PROMPT + "actualizar_producto(1, cantidad=8, precio=2350000)", CMD),
            ("'Producto 1 actualizado: cantidad=8, precio=2350000.'", RES),
            (PROMPT + "consultar_producto(1)   # verificacion", CMD),
            ("{'id': 1, 'nombre': 'Laptop HP 14', 'categoria': 'Electronica',", RES),
            (" 'cantidad': 8, 'precio': 2350000.0}", RES),
        ]
    ),
    (
        "cap4_listar_productos.png",
        "Prueba 4 — listar_productos",
        [
            (PROMPT + "listar_productos()", CMD),
            ("{'id': 1, 'nombre': 'Laptop HP 14',    'cantidad': 8,  'precio': 2350000.0}", RES),
            ("{'id': 2, 'nombre': 'Monitor Samsung 24','cantidad': 5, 'precio': 1200000.0}", RES),
            ("{'id': 3, 'nombre': 'Silla Ergonomica', 'cantidad': 0, 'precio':  850000.0}", RES),
            ("{'id': 4, 'nombre': 'Teclado Mecanico', 'cantidad': 20,'precio':  320000.0}", RES),
            ("{'id': 5, 'nombre': 'Mouse Inalambrico','cantidad': 15,'precio':  150000.0}", RES),
        ]
    ),
    (
        "cap5_valor_total.png",
        "Prueba 5 — calcular_valor_total_inventario",
        [
            (PROMPT + "calcular_valor_total_inventario()", CMD),
            ("{'valor_total_inventario': 33450000.0}", RES),
            ("", FG),
            ("  Calculo: (8×2350000) + (5×1200000) + (0×850000)", HDR),
            ("         + (20×320000) + (15×150000) = 33.450.000", HDR),
        ]
    ),
    (
        "cap6_agotados.png",
        "Prueba 6 — productos_agotados",
        [
            (PROMPT + "productos_agotados()", CMD),
            ("{'id': 3, 'nombre': 'Silla Ergonomica',", RES),
            (" 'categoria': 'Mobiliario', 'cantidad': 0, 'precio': 850000.0}", RES),
            ("", FG),
            ("  1 producto sin stock: Silla Ergonomica", HDR),
        ]
    ),
    (
        "cap7_mas_costoso.png",
        "Prueba 7 — producto_mas_costoso",
        [
            (PROMPT + "producto_mas_costoso()", CMD),
            ("{'id': 1, 'nombre': 'Laptop HP 14', 'categoria': 'Electronica',", RES),
            (" 'cantidad': 8, 'precio': 2350000.0}", RES),
        ]
    ),
    (
        "cap8_estadisticas.png",
        "Prueba 8 — estadisticas_inventario",
        [
            (PROMPT + "estadisticas_inventario()", CMD),
            ("{'total_productos':  5,", RES),
            (" 'precio_promedio':  974000.0,", RES),
            (" 'precio_minimo':    150000.0,", RES),
            (" 'precio_maximo':    2350000.0,", RES),
            (" 'unidades_totales': 48}", RES),
        ]
    ),
    (
        "cap9_eliminar_producto.png",
        "Prueba 9 — eliminar_producto",
        [
            (PROMPT + "eliminar_producto(2)", CMD),
            ("'Producto 2 eliminado del inventario.'", RES),
            (PROMPT + "listar_productos()   # verificacion post-eliminacion", CMD),
            ("{'id': 1, 'nombre': 'Laptop HP 14',    'cantidad': 8,  'precio': 2350000.0}", RES),
            ("{'id': 3, 'nombre': 'Silla Ergonomica','cantidad': 0,  'precio':  850000.0}", RES),
            ("{'id': 4, 'nombre': 'Teclado Mecanico','cantidad': 20, 'precio':  320000.0}", RES),
            ("{'id': 5, 'nombre': 'Mouse Inalambrico','cantidad': 15,'precio':  150000.0}", RES),
        ]
    ),
]

for fname, title, lines in capturas:
    render_terminal(lines, fname, title)

print("\nTodas las capturas generadas en:", OUT_DIR)
