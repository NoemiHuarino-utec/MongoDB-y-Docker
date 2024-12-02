from flask import Flask, request, jsonify
from MongoDBHandler import MongoDBHandler

app = Flask(__name__)
mongo_handler = MongoDBHandler()

'''
---------------------
      API CRUD:
---------------------
'''

# Obtener todos los productos
@app.route('/productos', methods=['GET'])
def get_all_products():
    products = mongo_handler.get_all_products()
    return jsonify(products), 200

# Obtener un producto específico por ID
@app.route('/productos/<id>', methods=['GET'])
def get_product_by_id(id):
    product = mongo_handler.get_product_by_id(id)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

# Crear un nuevo producto
@app.route('/productos', methods=['POST'])
def create_product():
    data = request.json
    result = mongo_handler.create_product(data)
    if result:
        return jsonify({"message": "Producto creado exitosamente"}), 201
    else:
        return jsonify({"error": "No se pudo crear el producto"}), 400

# Actualizar un producto por ID
@app.route('/productos/<id>', methods=['PUT'])
def update_product(id):
    data = request.json
    result = mongo_handler.update_product(id, data)
    if result:
        return jsonify({"message": "Producto actualizado exitosamente"}), 200
    else:
        return jsonify({"error": "No se pudo actualizar el producto"}), 400

# Eliminar un producto por ID
@app.route('/productos/<id>', methods=['DELETE'])
def delete_product(id):
    result = mongo_handler.delete_product(id)
    if result:
        return jsonify({"message": "Producto eliminado exitosamente"}), 200
    else:
        return jsonify({"error": "No se pudo eliminar el producto"}), 400


'''
---------------------
  CONSULTAS EXTRAS:
---------------------
'''

# Obtener productos agrupados por categoría
@app.route('/productos_por_categoria', methods=['GET'])
def get_products_by_category():
    grouped_products = mongo_handler.get_products_by_category()
    return jsonify(grouped_products), 200

# Obtener productos de una categoría específica
@app.route('/productos_por_categoria/<categoria>', methods=['GET'])
def get_products_by_specific_category(categoria):
    products = mongo_handler.get_products_by_specific_category(categoria)
    if products:
        return jsonify(products), 200
    else:
        return jsonify({"error": "No se encontraron productos para esta categoría"}), 404

# Obtener productos con stock menor a 10
@app.route('/productos_sin_stock', methods=['GET'])
def get_products_out_of_stock():
    low_stock_products = mongo_handler.get_products_out_of_stock()
    return jsonify(low_stock_products), 200

# Obtener productos con precio menor o igual a lo indicado
@app.route('/productos_precio/<precio>', methods=['GET'])
def get_products_by_price(precio):
    try:
        precio = float(precio)
        products = mongo_handler.get_products_by_price(precio)
        return jsonify(products), 200
    except ValueError:
        return jsonify({"error": "El precio debe ser un número válido"}), 400

# Obtener productos con el mejor review (rating: 5)
@app.route('/productos_best_review', methods=['GET'])
def get_products_best_review():
    best_reviewed_products = mongo_handler.get_products_best_review()
    return jsonify(best_reviewed_products), 200

# ----- Main -----
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Cambia el puerto si es necesario