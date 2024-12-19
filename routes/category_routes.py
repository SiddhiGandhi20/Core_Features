from flask import Blueprint, jsonify, request
from models.category_model import CategoryModel

# Define the Blueprint for category routes
category_bp = Blueprint("category", __name__)

def create_category_routes(db):
    category_model = CategoryModel(db)

    @category_bp.route("/categories", methods=["GET"])
    def get_categories():
        """Fetch all categories from the collection."""
        categories = category_model.get_all_categories()
        if not categories:
            return jsonify({"message": "No categories found or error fetching data"}), 500
        return jsonify(categories), 200
    
    @category_bp.route("/categories/name/<name>", methods=["GET"])
    def get_category_by_name(name):
        """Fetch a category by name."""
        category = category_model.get_category_by_name(name)
        if not category:
            return jsonify({"message": "Category not found"}), 404
        return jsonify(category), 200

    @category_bp.route("/categories/<category_id>", methods=["GET"])
    def get_category(category_id):
        """Fetch a single category by ID."""
        category = category_model.get_category_by_id(category_id)
        if not category:
            return jsonify({"message": "Category not found"}), 404
        return jsonify(category), 200

    @category_bp.route("/categories", methods=["POST"])
    def create_category():
        """Create a new category."""
        data = request.get_json()
        result = category_model.create_category(data)
        if result:
            return jsonify({"message": "Category created successfully", "category_id": result}), 201
        return jsonify({"message": "Error creating category"}), 500

    @category_bp.route("/categories/<category_id>", methods=["PUT"])
    def update_category(category_id):
        """Update a category by ID."""
        data = request.get_json()
        result = category_model.update_category(category_id, data)
        if result:
            return jsonify({"message": "Category updated successfully"}), 200
        return jsonify({"message": "Error updating category"}), 500

    @category_bp.route("/categories/<category_id>", methods=["DELETE"])
    def delete_category(category_id):
        """Delete a category by ID."""
        result = category_model.delete_category(category_id)
        if result:
            return jsonify({"message": "Category deleted successfully"}), 200
        return jsonify({"message": "Error deleting category"}), 500
    
    

    return category_bp
