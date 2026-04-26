from flask import Flask, jsonify, render_template
from flask_mysqldb import MySQL
#pip install flask_mysqldb

app = Flask(__name__)

mysql = MySQL(app)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "tienda_db_s2"

@app.route('/testdb')
def test():
    cursor = mysql.connection.cursor()
    sql = "SELECT 1"
    cursor.execute(sql)
    return "conexion exitosa!!!"

#@app.route('/')
#def inicio():
#    return "Servidor flask en ejecucion"

#ENDPOINT GET /CATEGORIAS
@app.route('/categorias', methods=['GET'])
def listar_categorias():
    cursor = mysql.connection.cursor()
    sql = "SELECT id, nombre FROM categoria"
    cursor.execute(sql)
    datos = cursor.fetchall()

    if datos == None:
        msg = {
            "mensage": "NO EXISTE CATEGORIA!!!"
        }
        return jsonify(msg)
    

    categorias = []
    for fila in datos:
        categorias.append(
            {
                "id": fila[0],
                "nombre": fila[1]
            }
        )
    cursor.close()
    return jsonify(categorias)

@app.route('/productos', methods=['GET'])
def listar_productos():
    cursor = mysql.connection.cursor()
    sql = "SELECT id, nombre, precio, stock, categoria_id FROM producto"
    cursor.execute(sql)
    datos = cursor.fetchall()

    if datos == None:
        msg = {
            "mensage": "NO EXISTE CATEGORIA!!!"
        }
        return jsonify(msg)
    

    productos = []
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": float(fila[2]),
                "stock": fila[3],
                "categoria_id": fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)

#ENDPOINT GET / productos/<id>
@app.route('/productos/<int:id>', methods=['GET'])
def producto_id(id):
    cursor = mysql.connection.cursor()
    sql ="""SELECT id, nombre, precio, stock, categoria_Id
            FROM producto 
            WHERE id = %s"""
    cursor.execute(sql, (id,))
    datos = cursor.fetchone()

    if datos == None:
        msg = {
            "mensage": "NO EXISTE PRODUCTO!!!"
        }
        return jsonify(msg)
    
    productos = []
    productos.append(
        {
            "id": datos[0],
            "nombre": datos[1],
            "precio": float(datos[2]),
            "stock": datos[3],
            "categoria_id": datos[4]
        }
    )
    cursor.close()
    return jsonify(productos)

@app.route('/productos_categoria', methods=['GET'])
def productos_con_categoria():
    cursor = mysql.connection.cursor()
    sql ="""SELECT p.id, p.nombre, p.precio, p.stock, c.nombre
            FROM producto p
            JOIN categoria c ON c.id = p.categoria_id"""
    cursor.execute(sql)
    datos = cursor.fetchall()

    if datos == None:
        msg = {
            "mensage": "NO EXISTE PRODUCTO!!!"
        }
        return jsonify(msg)
    
    productos = []
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": float(fila[2]),
                "stock": fila[3],
                "categoria": fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)

@app.route('/productos/categoria/<int:id>', methods=['GET'])
def producto_por_categoria_id(id):
    cursor = mysql.connection.cursor()
    sql ="""SELECT p.id, p.nombre, p.precio, p.stock, c.id
            FROM producto p
            JOIN categoria c ON c.id = p.categoria_id
            WHERE c.id = %s""" #es como un comodin que va a ser reemplazado por el parametro id 
    #puede ser tambien %s, %s, %s y abajo ponemos (id, precio, stock) por ejemplo
    cursor.execute(sql, (id,)) #este id va a reemplazar al %s
    datos = cursor.fetchall()

    if datos == None:
        msg = {
            "mensage": "NO EXISTE PRODUCTO!!!"
        }
        return jsonify(msg)
    
    productos = []
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": float(fila[2]),
                "stock": fila[3],
                "categoria": fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)

@app.route('/')
def inicio():
    return render_template('index.html')

#PRODUCTO MAS CARO
@app.route('/producto_mas_caro', methods=['GET'])
def producto_mas_caro():
    cursor = mysql.connection.cursor()
    sql = """SELECT id, nombre, precio, stock, categoria_id
            FROM producto 
            ORDER BY precio DESC
            LIMIT 1"""
    cursor.execute(sql)
    datos = cursor.fetchall()

    if datos == None:
        msg = {
            "mensage": "NO EXISTE PRODUCTO!!!"
        }
        return jsonify(msg)
    
    productos = []
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": float(fila[2]),
                "stock": fila[3],
                "categoria": fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)

#PRODUCTO CON POCO STOCK
@app.route('/productos/poco_stock', methods=['GET'])
def productos_poco_stock():
    cursor = mysql.connection.cursor()
    sql = """SELECT id, nombre, precio, stock, categoria_id
            FROM producto 
            WHERE stock <= 5"""
    cursor.execute(sql)
    datos = cursor.fetchall()

    if datos == None:
        msg = {
            "mensage": "NO EXISTE PRODUCTO!!!"
        }
        return jsonify(msg)

    productos = []
    for fila in datos:
        productos.append(
            {
                "id": fila[0],
                "nombre": fila[1],
                "precio": float(fila[2]),
                "stock": fila[3],
                "categoria": fila[4]
            }
        )
    cursor.close()
    return jsonify(productos)

#CANTIDAD DE PRODUCTOS POR CATEGORIA
@app.route('/cantidad_productos_por_categoria/<int:id>', methods=['GET'])
def cantidad_productos_por_categoria(id):
    cursor = mysql.connection.cursor()
    
    #Verificar si existe la categoría
    sql_categoria = "SELECT * FROM categoria WHERE id = %s"
    cursor.execute(sql_categoria, (id,))
    categoria = cursor.fetchone()

    if categoria == None:
        cursor.close()
        return jsonify({"mensaje": "NO EXISTE LA CATEGORIA!!!"}), 404

    sql = """SELECT COUNT(*) 
            FROM producto 
            WHERE categoria_id = %s"""
    cursor.execute(sql, (id,))
    cantidad = cursor.fetchone()[0]

    cursor.close()
    return jsonify({"Cantidad De Productos": cantidad})

if __name__ == "__main__":
    app.run(debug=True)















#def usuario():
#    return render_template(formulario, usuario=usuario)
