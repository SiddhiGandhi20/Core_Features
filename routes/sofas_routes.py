from flask import Blueprint, jsonify
from models.sofas_model import SofaModel

# Define the Blueprint for sofa routes
sofa_bp = Blueprint("sofa", __name__)

def create_sofa_routes(db):
    sofa_model = SofaModel(db)

    @sofa_bp.route("/sofas", methods=["GET"])
    def get_sofas():
        """Fetch all sofas from the collection."""
        sofas = sofa_model.get_all_sofas()
        if not sofas:
            return jsonify({"message": "No sofas found or error fetching data"}), 500
        return jsonify(sofas), 200

    return sofa_bp
