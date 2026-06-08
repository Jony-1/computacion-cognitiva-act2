# MCP Inventory Server — Actividad 6

**Jonathan Dario Sierra Galindo**  
Computación Cognitiva para Big Data  
Corporación Universitaria Iberoamericana  
Docente: Joaquin Sanchez

---

## Descripción

Servidor MCP (Model Context Protocol) para la gestión de un inventario de productos implementado con **FastMCP** y **SQLite3**. El servidor expone 9 herramientas que permiten crear, consultar, actualizar y eliminar productos, además de calcular estadísticas del inventario.

---

## Estructura del Proyecto

```
mcp_inventory/
├── database.py       # Inicialización de la base de datos SQLite
├── server.py         # Servidor MCP con las 9 herramientas
├── requirements.txt  # Dependencias del proyecto
└── README.md         # Este archivo
```

---

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Jony-1/computacion-cognitiva-act6.git
cd computacion-cognitiva-act6/mcp_inventory

# Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución

```bash
python server.py
```

---

## Herramientas MCP Disponibles

| Herramienta | Descripción |
|---|---|
| `crear_producto` | Inserta un nuevo producto en el inventario |
| `consultar_producto` | Busca un producto por ID |
| `actualizar_producto` | Actualiza cantidad y precio de un producto |
| `eliminar_producto` | Elimina un producto por ID |
| `listar_productos` | Lista todos los productos |
| `calcular_valor_total_inventario` | Calcula el valor total (cantidad × precio) |
| `productos_agotados` | Lista productos sin stock (cantidad = 0) |
| `producto_mas_costoso` | Devuelve el producto más caro |
| `estadisticas_inventario` | Estadísticas generales del inventario |

---

## Tecnologías

- Python 3.8+
- FastMCP 0.1+
- SQLite3 (incluido en Python)

---

## Licencia

Proyecto académico — Uso educativo.
