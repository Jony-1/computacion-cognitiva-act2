# MCP Inventory Server — Actividad 6

**Jonathan Dario Sierra Galindo**  
Computación Cognitiva para Big Data  
Corporación Universitaria Iberoamericana  
Docente: Joaquin Fernando Sanchez Cifuentes

---

## Descripción

Sistema completo de gestión de inventario que integra:
- **Servidor MCP** (Model Context Protocol) con FastMCP y SQLite3
- **Pipeline de datos**: generación → ETL → predicción de demanda
- **Dashboard web** en localhost:5002 con alertas de stock y estadísticas

---

## Estructura del Proyecto

```
mcp_inventory/
├── database.py            # Inicialización base de datos SQLite
├── server.py              # Servidor MCP con 9 herramientas
├── generar_datos.py       # Genera CSVs simulados (inventario, ventas)
├── etl.py                 # Proceso ETL: extrae, transforma, carga
├── modelo_prediccion.py   # Regresión lineal para predicción de demanda
├── app.py                 # Dashboard web — puerto 5002
├── requirements.txt       # Dependencias del proyecto
├── data/                  # Archivos CSV generados
│   ├── inventario.csv
│   ├── productos.csv
│   ├── ventas.csv
│   ├── ventas_procesadas.csv
│   └── predicciones.csv
└── capturas/              # Screenshots de cada operación probada
```

---

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/Jony-1/computacion-cognitiva-act2.git
cd computacion-cognitiva-act2/mcp_inventory

# Crear entorno virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución paso a paso

```bash
# 1. Generar datos simulados
python generar_datos.py

# 2. Ejecutar ETL
python etl.py

# 3. Ejecutar modelo de predicción
python modelo_prediccion.py

# 4. Iniciar dashboard web
python app.py
# → Abrir http://localhost:5002

# 5. Iniciar servidor MCP (para conectar con LLM)
python server.py
```

---

## Herramientas MCP (server.py)

| Herramienta | Descripción |
|---|---|
| `crear_producto` | Inserta nuevo producto en SQLite |
| `consultar_producto` | Busca por ID |
| `actualizar_producto` | Actualiza cantidad y precio |
| `eliminar_producto` | Elimina por ID |
| `listar_productos` | Lista todo el inventario |
| `calcular_valor_total_inventario` | Suma (cantidad × precio) |
| `productos_agotados` | Productos con cantidad = 0 |
| `producto_mas_costoso` | Producto con precio más alto |
| `estadisticas_inventario` | Promedio, min, max, totales |

---

## Dashboard Web

Acceder a `http://localhost:5002` para ver:
- KPIs: unidades vendidas, ingresos, alertas de stock
- Tabla de alertas de stock (cantidad < stock mínimo)
- Top 5 productos más vendidos (90 días)
- Predicción de demanda para la próxima semana

---

## Tecnologías

- Python 3.8+
- FastMCP 3.4+
- SQLite3 (stdlib)
- CSV (stdlib)
- http.server (stdlib — dashboard sin dependencias extra)

---

## Licencia

Proyecto académico — Uso educativo.
