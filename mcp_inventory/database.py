import sqlite3

# Nombre del archivo de base de datos
NOMBRE_BD = "inventario.db"

def inicializar_bd():
    """Crea la tabla de productos si no existe todavia."""
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    # Tabla principal del inventario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre    TEXT    NOT NULL,
            categoria TEXT,
            cantidad  INTEGER NOT NULL,
            precio    REAL    NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()
    print("Base de datos lista:", NOMBRE_BD)

if __name__ == "__main__":
    inicializar_bd()
