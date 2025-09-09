from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Función para establecer la conexión con la base de datos
def db_connection():
	conn = None
	try:
		# Conectamos a nuestra base de datos del restaurante
		conn = sqlite3.connect('restaurant.sqlite')
	except sqlite3.error as e:
		print(e)
	return conn

# Ruta para obtener todo el menú (GET) y crear un nuevo plato (POST)
@app.route("/menu" , methods=["GET","POST"])
def menu():
	conn = db_connection()
	cursor = conn.cursor()

	# Método GET: Obtener todos los platos del menú
	if request.method == "GET":
		cursor = conn.execute("SELECT * FROM menu")
		# Adaptamos los campos a nuestra tabla 'menu'
		menu_items = [
		  dict(id=row[0], nombre=row[1], descripcion=row[2], precio=row[3], categoria=row[4])
		  for row in cursor.fetchall()
		]
		if menu_items is not None:
			return jsonify(menu_items)

	# Método POST: Crear un nuevo plato en el menú
	if request.method == "POST":
		# Obtenemos los datos del formulario (form-data)
		nombre = request.form["nombre"]
		descripcion = request.form["descripcion"]
		precio = request.form["precio"]
		categoria  = request.form["categoria"]

		# Consulta SQL para INSERTAR un nuevo plato en la base de datos
		sql = """INSERT INTO menu (nombre, descripcion, precio, categoria)
				 VALUES (?, ?, ?, ?) """
		cursor = cursor.execute(sql, (nombre, descripcion, precio, categoria))
		conn.commit()
		return f"Plato con id: {cursor.lastrowid} creado exitosamente."

# Ruta para obtener, actualizar y eliminar un plato específico por su ID
@app.route('/menu/<int:id>', methods=["GET", "PUT", "DELETE"])
def single_menu_item(id):
	conn = db_connection()
	cursor = conn.cursor()
	menu_item = None

	# Método GET: Obtener un solo plato por su ID
	if request.method == "GET":
		cursor.execute("SELECT * FROM menu WHERE id=?", (id,))
		row = cursor.fetchone()
		if row is not None:
			menu_item = dict(id=row[0], nombre=row[1], descripcion=row[2], precio=row[3], categoria=row[4])
			return jsonify(menu_item), 200
		else:
			return "Plato no encontrado", 404

	# Método PUT: Actualizar un plato existente
	if request.method == "PUT":
		sql = """ UPDATE menu
				  SET nombre = ?,
					  descripcion = ?,
					  precio = ?,
					  categoria = ?
				  WHERE id = ? """

		# Obtenemos los nuevos datos del formulario
		nombre = request.form["nombre"]
		descripcion = request.form["descripcion"]
		precio = request.form["precio"]
		categoria = request.form["categoria"]

		updated_item = {
			"id": id,
			"nombre": nombre,
			"descripcion": descripcion,
			"precio": precio,
			"categoria": categoria
		}
		conn.execute(sql, (nombre, descripcion, precio, categoria, id))
		conn.commit()
		return jsonify(updated_item)

	# Método DELETE: Eliminar un plato
	if request.method == "DELETE":
		sql = """ DELETE FROM menu WHERE id=? """
		conn.execute(sql, (id,))
		conn.commit()
		return f"El plato con id: {id} ha sido eliminado.", 200

if __name__ == '__main__':
   # Usamos host='0.0.0.0' para que la API sea accesible desde la red (clave para EC2)
   # y debug=True para ver los errores durante el desarrollo
   app.run(host='0.0.0.0', port=8000, debug=True)
