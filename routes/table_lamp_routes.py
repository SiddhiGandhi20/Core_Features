from flask import Blueprint, jsonify
from models.table_lamp_model import TableLampModel

# Define the Blueprint for table lamp routes
table_lamp_bp = Blueprint("table_lamp", __name__)

def create_table_lamp_routes(db):
    table_lamp_model = TableLampModel(db)

    @table_lamp_bp.route("/table_lamps", methods=["GET"])
    def get_table_lamps():
        """Fetch all table lamps from the collection."""
        table_lamps = table_lamp_model.get_all_table_lamps()
        if not table_lamps:
            return jsonify({"message": "No table lamps found or error fetching data"}), 500
        return jsonify(table_lamps), 200

    return table_lamp_bp
