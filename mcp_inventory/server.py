# Servidor MCP para gestion de inventario
# MCP = Model Context Protocol, permite que un LLM use nuestras funciones como herramientas
# Actividad 6 - Computacion Cognitiva para Big Data
# Jonathan Dario Sierra Galindo

# fastmcp es la libreria que hace todo el trabajo del protocolo MCP
# con @mcp.tool() le decimos al modelo cuales funciones puede usar
from fastmcp import FastMCP
import sqlite3  # para conectarnos a la base de datos

# importamos las cosas que creamos en database.py
from database import NOMBRE_BD, inicializar_bd

# creamos el servidor y le damos un nombre
# este nombre aparece cuando el modelo se conecta al servidor
mcp = FastMCP("Servidor Inventario")

# antes de hacer cualquier cosa, nos aseguramos de que la BD exista
inicializar_bd()


# -------------------------------------------------------
# funcion de ayuda para no repetir el codigo de conexion
# -------------------------------------------------------
def obtener_conexion():
    # sqlite3.Row hace que los resultados se puedan leer como diccionarios
    # por ejemplo: fila["nombre"] en vez de fila[1]
    conexion = sqlite3.connect(NOMBRE_BD)
    conexion.row_factory = sqlite3.Row
    return conexion


# -------------------------------------------------------
# HERRAMIENTA 1: crear un producto nuevo
# -------------------------------------------------------
@mcp.tool()
def crear_producto(nombre: str, categoria: str, cantidad: int, precio: float) -> str:
    # primero validamos que los datos tengan sentido
    # no tiene sentido tener cantidad o precio negativos
    if cantidad < 0:
        return "Error: la cantidad no puede ser negativa."
    if precio < 0:
        return "Error: el precio no puede ser negativo."

    # abrimos la conexion y ejecutamos el INSERT
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # los signos ? son marcadores de posicion para evitar inyeccion SQL
    cursor.execute(
        "INSERT INTO productos (nombre, categoria, cantidad, precio) VALUES (?, ?, ?, ?)",
        (nombre, categoria, cantidad, precio)
    )

    # guardamos el cambio en el archivo
    conexion.commit()

    # lastrowid nos dice el ID que le asigno la base de datos al nuevo registro
    nuevo_id = cursor.lastrowid
    conexion.close()

    return f"Producto creado correctamente con ID {nuevo_id}."


# -------------------------------------------------------
# HERRAMIENTA 2: buscar un producto por su ID
# -------------------------------------------------------
@mcp.tool()
def consultar_producto(producto_id: int) -> dict:
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # SELECT * trae todas las columnas del producto que tenga ese id
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    fila = cursor.fetchone()  # fetchone trae solo un resultado (el primero)
    conexion.close()

    # si no encontro nada, fetchone devuelve None
    if fila is None:
        return {"error": f"No se encontro ningun producto con ID {producto_id}."}

    # convertimos el resultado a diccionario para que sea facil de leer
    return dict(fila)


# -------------------------------------------------------
# HERRAMIENTA 3: actualizar cantidad y precio
# -------------------------------------------------------
@mcp.tool()
def actualizar_producto(producto_id: int, cantidad: int, precio: float) -> str:
    if cantidad < 0:
        return "Error: la cantidad no puede ser negativa."
    if precio < 0:
        return "Error: el precio no puede ser negativo."

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # UPDATE modifica los campos que le digamos para el registro con ese id
    cursor.execute(
        "UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
        (cantidad, precio, producto_id)
    )
    conexion.commit()

    # rowcount dice cuantos registros fueron afectados
    # si es 0 significa que no habia ningun producto con ese id
    filas_afectadas = cursor.rowcount
    conexion.close()

    if filas_afectadas == 0:
        return f"No existe producto con ID {producto_id}."

    return f"Producto {producto_id} actualizado: cantidad={cantidad}, precio={precio}."


# -------------------------------------------------------
# HERRAMIENTA 4: borrar un producto
# -------------------------------------------------------
@mcp.tool()
def eliminar_producto(producto_id: int) -> str:
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # DELETE borra el registro que tenga ese id
    cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conexion.commit()

    filas_afectadas = cursor.rowcount
    conexion.close()

    if filas_afectadas == 0:
        return f"No se encontro producto con ID {producto_id} para eliminar."

    return f"Producto {producto_id} eliminado del inventario."


# -------------------------------------------------------
# HERRAMIENTA 5: ver todos los productos
# -------------------------------------------------------
@mcp.tool()
def listar_productos() -> list:
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # ORDER BY id para que siempre salgan en el mismo orden
    cursor.execute("SELECT * FROM productos ORDER BY id")

    # fetchall trae todos los resultados de una vez como lista
    filas = cursor.fetchall()
    conexion.close()

    # convertimos cada fila a diccionario y devolvemos la lista completa
    return [dict(f) for f in filas]


# -------------------------------------------------------
# HERRAMIENTA 6: calcular cuanto vale todo el inventario
# -------------------------------------------------------
@mcp.tool()
def calcular_valor_total_inventario() -> dict:
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # SUM(cantidad * precio) hace la multiplicacion y suma todo en un solo paso
    cursor.execute("SELECT SUM(cantidad * precio) AS valor_total FROM productos")
    resultado = cursor.fetchone()
    conexion.close()

    # si el inventario esta vacio, SUM devuelve None, por eso usamos 'or 0.0'
    valor = resultado["valor_total"] if resultado["valor_total"] else 0.0

    return {"valor_total_inventario": round(valor, 2)}


# -------------------------------------------------------
# HERRAMIENTA 7: ver que productos no tienen stock
# -------------------------------------------------------
@mcp.tool()
def productos_agotados() -> list:
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # traemos solo los productos que tienen cantidad = 0
    cursor.execute("SELECT * FROM productos WHERE cantidad = 0 ORDER BY nombre")
    filas = cursor.fetchall()
    conexion.close()

    return [dict(f) for f in filas]


# -------------------------------------------------------
# HERRAMIENTA 8: encontrar el producto mas caro
# -------------------------------------------------------
@mcp.tool()
def producto_mas_costoso() -> dict:
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # ORDER BY precio DESC ordena de mayor a menor, LIMIT 1 trae solo el primero
    cursor.execute("SELECT * FROM productos ORDER BY precio DESC LIMIT 1")
    fila = cursor.fetchone()
    conexion.close()

    if fila is None:
        return {"error": "El inventario esta vacio."}

    return dict(fila)


# -------------------------------------------------------
# HERRAMIENTA 9: estadisticas generales del inventario
# -------------------------------------------------------
@mcp.tool()
def estadisticas_inventario() -> dict:
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # usamos funciones de agregacion de SQL:
    # COUNT = contar registros
    # AVG = promedio
    # MIN y MAX = minimo y maximo
    # SUM = suma total
    cursor.execute("""
        SELECT
            COUNT(*)      AS total_productos,
            AVG(precio)   AS precio_promedio,
            MIN(precio)   AS precio_minimo,
            MAX(precio)   AS precio_maximo,
            SUM(cantidad) AS unidades_totales
        FROM productos
    """)

    fila = cursor.fetchone()
    conexion.close()

    # el 'or 0' es por si el inventario esta vacio y devuelve None
    return {
        "total_productos":  fila["total_productos"],
        "precio_promedio":  round(fila["precio_promedio"] or 0, 2),
        "precio_minimo":    fila["precio_minimo"] or 0,
        "precio_maximo":    fila["precio_maximo"] or 0,
        "unidades_totales": fila["unidades_totales"] or 0,
    }


# esto arranca el servidor cuando ejecutamos: python server.py
if __name__ == "__main__":
    mcp.run()
