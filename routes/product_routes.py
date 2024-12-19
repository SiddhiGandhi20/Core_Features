from flask import Blueprint, request, jsonify
from models.product_model import ProductModel
from models.category_model import CategoryModel

# Define the Blueprint for product routes
product_bp = Blueprint("product", __name__)

def create_product_routes(db):
    product_model = ProductModel(db)
    category_model = CategoryModel(db)

    # Create Product (POST)
    @product_bp.route("/products", methods=["POST"])
    def create_product():
        """Create a new product in the database."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"message": "No data provided"}), 400

            # Ensure required fields are present
            required_fields = ["name", "description", "price", "category", "image_url", "stock_quantity"]
            for field in required_fields:
                if field not in data:
                    return jsonify({"message": f"Missing {field} in request data"}), 400

            response, status = product_model.create_product(data)

            return jsonify(response), status

        except Exception as e:
            print(f"Error creating product: {e}")
            return jsonify({"message": f"Error creating product: {str(e)}"}), 500

    # Read Product (GET)
    @product_bp.route("/products/<product_id>", methods=["GET"])
    def get_product(product_id):
        """Fetch a single product by its ID."""
        try:
            product = product_model.get_product_by_id(product_id)
            if product:
                return jsonify(product), 200
            return jsonify({"message": "Product not found"}), 404
        except Exception as e:
            print(f"Error fetching product: {e}")
            return jsonify({"message": f"Error fetching product: {str(e)}"}), 500

    # Get All Products (GET)
    @product_bp.route("/products", methods=["GET"])
    def get_all_products():
        """Fetch all products from the collection."""
        try:
            products = product_model.get_all_products()
            if not products:
                return jsonify({"message": "No products found"}), 404
            return jsonify(products), 200
        except Exception as e:
            print(f"Error fetching products: {e}")
            return jsonify({"message": f"Error fetching products: {str(e)}"}), 500

    # Update Product (PUT)
    @product_bp.route("/products/<product_id>", methods=["PUT"])
    def update_product(product_id):
        """Update product details."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"message": "No data provided"}), 400

            updated_product, status = product_model.update_product(product_id, data)

            return jsonify(updated_product), status

        except Exception as e:
            print(f"Error updating product: {e}")
            return jsonify({"message": f"Error updating product: {str(e)}"}), 500

    # Delete Product (DELETE)
    @product_bp.route("/products/<product_id>", methods=["DELETE"])
    def delete_product(product_id):
        """Delete a product by its ID."""
        try:
            result, status = product_model.delete_product(product_id)
            return jsonify(result), status
        except Exception as e:
            print(f"Error deleting product: {e}")
            return jsonify({"message": f"Error deleting product: {str(e)}"}), 500

    # New route for getting category by name
   # In product_routes.py or equivalent
    # In product_routes.py or equivalent

    @product_bp.route("/products/category/<category_name>", methods=["GET"])
    def get_products_by_category_name(category_name):
        """Fetch all products belonging to a category by category name."""
        products = product_model.get_products_by_category_name(category_name)
        if not products:
            return jsonify({"message": "No products found in this category"}), 404
        return jsonify(products), 200

    return product_bp
