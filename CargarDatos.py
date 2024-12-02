from MongoDBHandler import MongoDBHandler

# Uso de la clase
if __name__ == "__main__":
    # URL del JSON para las categorías
    categories_url = "https://dummyjson.com/products/categories"

    # Crear instancia de MongoDBHandler 
    mongo_handler = MongoDBHandler()
    
    # 1. Obtener todas las categorías
    print("Cargando las categorías desde la API.")
    mongo_handler.fetch_all_categories(categories_url)  
    print("Categorías terminaron de cargar.")
    
    # 2. Obtener todos los productos por categoría
    print("Cargando los productos desde la API por categoría.")
    mongo_handler.fetch_all_products()
    print("Productos terminaron de cargar.")
