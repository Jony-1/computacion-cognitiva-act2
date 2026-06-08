"""
Servidor MCP para gestión de inventario con SQLite.
Actividad 6 — Computación Cognitiva para Big Data
Jonathan Dario Sierra Galindo
"""

from fastmcp import FastMCP
import sqlite3
from database import NOMBRE_BD, inicializar_bd

# Crear instancia del servidor MCP
mcp = FastMCP("Servidor Inventario")

# Inicializar la base de datos al arrancar
inicializar_bd()


# ─────────────────────────────────────────────
# Funcion auxiliar para obtener conexion
# ─────────────────────────────────────────────
def obtener_conexion():
    """Devuelve una conexion con row_factory para obtener dicts."""
    conexion = sqlite3.connect(NOMBRE_BD)
    conexion.row_factory = sqlite3.Row
    return conexion


# ─────────────────────────────────────────────
# CRUD basico
# ─────────────────────────────────────────────

@mcp.tool()
def crear_producto(nombre: str, categoria: str, cantidad: int, precio: float) -> str:
    """Inserta un nuevo producto en el inventario."""
    if cantidad < 0:
        return "Error: la cantidad no puede ser negativa."
    if precio < 0:
        return "Error: el precio no puede ser negativo."

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, categoria, cantidad, precio) VALUES (?, ?, ?, ?)",
        (nombre, categoria, cantidad, precio)
    )
    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()
    return f"Producto creado correctamente con ID {nuevo_id}."


@mcp.tool()
def consultar_producto(producto_id: int) -> dict:
    """Busca un producto por su ID y retorna sus datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    fila = cursor.fetchone()
    conexion.close()

    if fila is None:
        return {"error": f"No se encontro ningun producto con ID {producto_id}."}

    return dict(fila)


@mcp.tool()
def actualizar_producto(producto_id: int, cantidad: int, precio: float) -> str:
    """Actualiza la cantidad y el precio de un producto existente."""
    if cantidad < 0:
        return "Error: la cantidad no puede ser negativa."
    if precio < 0:
        return "Error: el precio no puede ser negativo."

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
        (cantidad, precio, producto_id)
    )
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()

    if filas_afectadas == 0:
        return f"No existe producto con ID {producto_id}."
    return f"Producto {producto_id} actualizado: cantidad={cantidad}, precio={precio}."


@mcp.tool()
def eliminar_producto(producto_id: int) -> str:
    """Elimina un producto del inventario segun su ID."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()

    if filas_afectadas == 0:
        return f"No se encontro producto con ID {producto_id} para eliminar."
    return f"Producto {producto_id} eliminado del inventario."


@mcp.tool()
def listar_productos() -> list:
    """Retorna todos los productos del inventario."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY id")
    filas = cursor.fetchall()
    conexion.close()
    return [dict(f) for f in filas]


# ─────────────────────────────────────────────
# Herramientas de analisis
# ─────────────────────────────────────────────

@mcp.tool()
def calcular_valor_total_inventario() -> dict:
    """Calcula el valor total del inventario (cantidad * precio por producto)."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT SUM(cantidad * precio) AS valor_total FROM productos")
    resultado = cursor.fetchone()
    conexion.close()

    valor = resultado["valor_total"] if resultado["valor_total"] else 0.0
    return {"valor_total_inventario": round(valor, 2)}


@mcp.tool()
def productos_agotados() -> list:
    """Lista todos los productos con cantidad igual a cero (sin stock)."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad = 0 ORDER BY nombre")
    filas = cursor.fetchall()
    conexion.close()
    return [dict(f) for f in filas]


@mcp.tool()
def producto_mas_costoso() -> dict:
    """Devuelve el producto con el precio unitario mas alto."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY precio DESC LIMIT 1")
    fila = cursor.fetchone()
    conexion.close()

    if fila is None:
        return {"error": "El inventario esta vacio."}
    return dict(fila)


@mcp.tool()
def estadisticas_inventario() -> dict:
    """Calcula estadisticas generales: total productos, precio promedio, min y max."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT
            COUNT(*)       AS total_productos,
            AVG(precio)    AS precio_promedio,
            MIN(precio)    AS precio_minimo,
            MAX(precio)    AS precio_maximo,
            SUM(cantidad)  AS unidades_totales
        FROM productos
    """)
    fila = cursor.fetchone()
    conexion.close()

    return {
        "total_productos":  fila["total_productos"],
        "precio_promedio":  round(fila["precio_promedio"] or 0, 2),
        "precio_minimo":    fila["precio_minimo"] or 0,
        "precio_maximo":    fila["precio_maximo"] or 0,
        "unidades_totales": fila["unidades_totales"] or 0,
    }


# ─────────────────────────────────────────────
# Punto de entrada
# ─────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
