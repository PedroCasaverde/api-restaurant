import sqlite3

# Crear la conexión a la base de datos (creará el archivo si no existe)
conn = sqlite3.connect("restaurant.sqlite")

# Crear un objeto cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Consulta SQL para crear la tabla 'menu' con campos relevantes para un restaurante
# Usamos REAL para el precio, que es más adecuado para valores decimales.
sql_query = """ CREATE TABLE menu (
	id INTEGER PRIMARY KEY,
	nombre TEXT NOT NULL,
	descripcion TEXT NOT NULL,
	precio REAL NOT NULL,
	categoria TEXT NOT NULL
)"""

# Ejecutar la consulta para crear la tabla
cursor.execute(sql_query)

print("Base de datos 'restaurant.sqlite' y tabla 'menu' creadas exitosamente.")
