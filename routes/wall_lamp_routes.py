from flask import Blueprint, jsonify
from models.wall_lamp_model import WallLampModel

# Define the Blueprint for wall lamp routes
wall_lamp_bp = Blueprint("wall_lamp", __name__)

def create_wall_lamp_routes(db):
    wall_lamp_model = WallLampModel(db)

    @wall_lamp_bp.route("/wall_lamps", methods=["GET"])
    def get_wall_lamps():
        """Fetch all wall lamps from the collection."""
        wall_lamps = wall_lamp_model.get_all_wall_lamps()
        if not wall_lamps:
            return jsonify({"message": "No wall lamps found or error fetching data"}), 500
        return jsonify(wall_lamps), 200

    return wall_lamp_bp
