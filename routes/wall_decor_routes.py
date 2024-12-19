from flask import Blueprint, jsonify
from models.wall_decor_model import WallDecorModel

# Define the Blueprint for wall decor routes
wall_decor_bp = Blueprint("wall_decor", __name__)

def create_wall_decor_routes(db):
    wall_decor_model = WallDecorModel(db)

    @wall_decor_bp.route("/wall_decor", methods=["GET"])
    def get_wall_decor():
        """Fetch all wall decor items from the collection."""
        wall_decor_items = wall_decor_model.get_all_wall_decor()
        if not wall_decor_items:
            return jsonify({"message": "No wall decor found or error fetching data"}), 500
        return jsonify(wall_decor_items), 200

    return wall_decor_bp
