from flask import Blueprint, jsonify
from models.beds_models import BedsModel

# Blueprint setup for Beds routes
beds_bp = Blueprint("beds", __name__)

def create_beds_routes(db):
    beds_model = BedsModel(db)

    @beds_bp.route("/beds", methods=["GET"])
    def get_all_beds():
        """Fetch all beds from the collection."""
        beds = beds_model.get_all_beds()
        if not beds:
            return jsonify({"message": "No beds found or error fetching data"}), 500
        return jsonify(beds), 200

    return beds_bp
