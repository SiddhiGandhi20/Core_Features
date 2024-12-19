from bson import ObjectId
from models.category_model import CategoryModel

class ProductModel:
    def __init__(self, db):
        self.collection = db.products  # Access the 'products' collection in MongoDB
        self.category_model = CategoryModel(db)  # Initialize CategoryModel for checking category

    # Create a new product
    def create_product(self, data):
        try:
            category_name = data["category"]

            # Check if category already exists
            existing_category = self.category_model.get_category_by_name(category_name)
            if not existing_category:
                # Create new category if it doesn't exist
                self.category_model.collection.insert_one({
                    "name": category_name,
                    "description": data.get("description", "")
                })

            # Prepare product data
            product_data = {
                "name": data["name"],
                "description": data["description"],
                "price": data["price"],
                "category": category_name,
                "image_url": data["image_url"],
                "stock_quantity": data["stock_quantity"]
            }
            result = self.collection.insert_one(product_data)
            product_id = str(result.inserted_id)  # Convert ObjectId to string

            return {"message": "Product created successfully", "product_id": product_id}, 201

        except Exception as e:
            print(f"Error creating product: {e}")
            return {"message": "Error creating product", "error": str(e)}, 500

    # Get a product by ID
    def get_product_by_id(self, product_id):
        try:
            product = self.collection.find_one({"_id": ObjectId(product_id)})
            if product:
                product["_id"] = str(product["_id"])  # Convert ObjectId to string for JSON serialization
                return product
            return None
        except Exception as e:
            print(f"Error fetching product: {e}")
            return None

    # Get all products
    def get_all_products(self):
        try:
            products = list(self.collection.find())
            for product in products:
                product["_id"] = str(product["_id"])  # Convert ObjectId to string for JSON serialization
            return products
        except Exception as e:
            print(f"Error fetching products: {e}")
            return None

    # Update a product by ID
    def update_product(self, product_id, data):
        try:
            update_data = {key: value for key, value in data.items() if value is not None}
            result = self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
            
            if result.modified_count == 0:
                return {"message": "Product not found or no changes made"}, 404
            
            updated_product = self.collection.find_one({"_id": ObjectId(product_id)})
            updated_product["_id"] = str(updated_product["_id"])  # Convert ObjectId to string
            return updated_product, 200
        except Exception as e:
            print(f"Error updating product: {e}")
            return {"message": "Error updating product", "error": str(e)}, 500

    # Delete a product by ID
    def delete_product(self, product_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(product_id)})
            
            if result.deleted_count == 0:
                return {"message": "Product not found"}, 404

            return {"message": "Product deleted successfully"}, 200
        except Exception as e:
            print(f"Error deleting product: {e}")
            return {"message": "Error deleting product", "error": str(e)}, 500

    def get_products_by_category_name(self, category_name):
        """Fetch products by category name."""
        try:
            products = list(self.collection.find({"category": category_name}))
            for product in products:
                product["_id"] = str(product["_id"])  # Convert ObjectId to string
            return products
        except Exception as e:
            print(f"Error fetching products by category: {e}")
            return None