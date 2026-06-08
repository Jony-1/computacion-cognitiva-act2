# Este archivo se encarga de crear la base de datos y la tabla que vamos a usar
# SQLite es una base de datos que guarda todo en un solo archivo .db
# No necesita instalar ningun servidor aparte, python ya lo trae incluido

import sqlite3  # este modulo viene con python, no hay que instalarlo

# Aqui definimos el nombre del archivo donde se van a guardar los datos
# si el archivo no existe, sqlite lo crea solo la primera vez
NOMBRE_BD = "inventario.db"


def inicializar_bd():
    # Esta funcion crea la tabla 'productos' si todavia no existe
    # Si ya existe no pasa nada, por eso usamos IF NOT EXISTS

    # primero abrimos la conexion con el archivo de base de datos
    conexion = sqlite3.connect(NOMBRE_BD)

    # el cursor es como el lapiz que escribe en la base de datos
    cursor = conexion.cursor()

    # creamos la tabla con sus columnas:
    # id: numero unico que se asigna solo (autoincrement)
    # nombre: texto obligatorio del producto
    # categoria: texto opcional para clasificar el producto
    # cantidad: cuantas unidades hay en bodega
    # precio: precio unitario del producto
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre    TEXT    NOT NULL,
            categoria TEXT,
            cantidad  INTEGER NOT NULL,
            precio    REAL    NOT NULL
        )
    """)

    # guardamos los cambios en el archivo
    conexion.commit()

    # cerramos la conexion para liberar el archivo
    conexion.close()

    print("Base de datos lista:", NOMBRE_BD)


# esto hace que si ejecutamos este archivo directamente, cree la BD
if __name__ == "__main__":
    inicializar_bd()
