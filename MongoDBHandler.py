#MongoDBHandler.py

import requests
from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDBHandler:
    def __init__(self):
        self.mongo_uri = "mongodb://localhost:27017/"
        self.db_name = "utec_store"
        self.categories_name = "categorias"
        self.products_name = "productos"
        self.connect_mongo()

    # Conectar a MongoDB
    def connect_mongo(self):
        try:
            client = MongoClient(self.mongo_uri)
            self.db = client[self.db_name]
            print(f"Conectado a la base de datos '{self.db_name}' en MongoDB.")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")

    # Obtener datos JSON desde la URL
    def fetch_json_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de {url}: {e}")
        return None

    # Obtener todas las categorías
    def fetch_all_categories(self, base_url):
        categories = self.fetch_json_data(base_url)
        if categories:
            self.insert_categories(categories)
            print(f"Categorías cargadas: {categories}")
        else:
            print("No se pudieron cargar las categorías.")

    # Insertar categorías en MongoDB
    def insert_categories(self, categories):
        try:
            collection = self.db[self.categories_name]
            collection.delete_many({})  # Limpia la colección antes de insertar
            data = [{"categoria": category} for category in categories]
            collection.insert_many(data)
            print(f"Se insertaron {len(data)} categorías en MongoDB.")
        except Exception as e:
            print(f"Error al insertar categorías: {e}")

    # Obtener todos los productos
    def fetch_all_products(self):
        try:
            categories = self.db[self.categories_name].find()
            for category in categories:
                category_name = category["categoria"]
                url = f"https://dummyjson.com/products/category/{category_name}?limit=0"
                products = self.fetch_json_data(url)
                if products and "products" in products:
                    self.insert_products(products["products"], category_name)
        except Exception as e:
            print(f"Error al cargar productos: {e}")

    # Insertar productos en MongoDB
    def insert_products(self, products, category_name):
        try:
            collection = self.db[self.products_name]
            for product in products:
                product["categoria"] = category_name
            collection.insert_many(products)
            print(f"Se insertaron {len(products)} productos en la categoría '{category_name}'.")
        except Exception as e:
            print(f"Error al insertar productos: {e}")

    # Obtener todos los productos (para la API)
    def get_all_products(self):
        try:
            collection = self.db[self.products_name]
            return list(collection.find({}, {"_id": 0}))  # Excluir el campo _id
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []

    # Obtener un producto por ID
    def get_product_by_id(self, product_id):
        try:
            collection = self.db[self.products_name]
            return collection.find_one({"_id": ObjectId(product_id)})
        except Exception as e:
            print(f"Error al obtener el producto: {e}")
            return None

    # Crear un producto
    def create_product(self, product):
        try:
            collection = self.db[self.products_name]
            return collection.insert_one(product).inserted_id
        except Exception as e:
            print(f"Error al crear producto: {e}")
            return None

    # Actualizar un producto por ID
    def update_product(self, product_id, updates):
        try:
            collection = self.db[self.products_name]
            result = collection.update_one({"_id": ObjectId(product_id)}, {"$set": updates})
            return result.modified_count
        except Exception as e:
            print(f"Error al actualizar el producto: {e}")
            return None

    # Eliminar un producto por ID
    def delete_product(self, product_id):
        try:
            collection = self.db[self.products_name]
            result = collection.delete_one({"_id": ObjectId(product_id)})
            return result.deleted_count
        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
            return None

    # Consultas avanzadas
    def get_products_grouped_by_category(self):
        try:
            collection = self.db[self.products_name]
            return list(collection.aggregate([
                {"$group": {"_id": "$categoria", "productos": {"$push": "$$ROOT"}}}
            ]))
        except Exception as e:
            print(f"Error al agrupar productos: {e}")
            return []

    def get_products_by_category(self, category):
        try:
            collection = self.db[self.products_name]
            return list(collection.find({"categoria": category}, {"_id": 0}))
        except Exception as e:
            print(f"Error al obtener productos por categoría: {e}")
            return []

    def get_products_out_of_stock(self):
        try:
            collection = self.db[self.products_name]
            return list(collection.find({"stock": {"$lt": 10}}, {"_id": 0}))
        except Exception as e:
            print(f"Error al obtener productos sin stock: {e}")
            return []

    def get_products_by_price(self, price):
        try:
            collection = self.db[self.products_name]
            return list(collection.find({"price": {"$lte": price}}, {"_id": 0}))
        except Exception as e:
            print(f"Error al obtener productos por precio: {e}")
            return []

    def get_best_reviewed_products(self):
        try:
            collection = self.db[self.products_name]
            return list(collection.find({"rating": {"$gte": 5}}, {"_id": 0}))
        except Exception as e:
            print(f"Error al obtener productos mejor calificados: {e}")
            return []
