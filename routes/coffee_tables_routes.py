from flask import Blueprint, jsonify
from models.coffee_tables_model import CoffeeTableModel

# Define the Blueprint for coffee_table routes
coffee_table_bp = Blueprint("coffee_table", __name__)

def create_coffee_table_routes(db):
    coffee_table_model = CoffeeTableModel(db)

    @coffee_table_bp.route("/coffee_tables", methods=["GET"])
    def get_coffee_tables():
        """Fetch all coffee tables from the collection."""
        coffee_tables = coffee_table_model.get_all_coffee_tables()
        if not coffee_tables:
            return jsonify({"message": "No coffee tables found or error fetching data"}), 500
        return jsonify(coffee_tables), 200

    return coffee_table_bp
