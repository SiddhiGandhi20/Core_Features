from flask import Blueprint, request, jsonify
import re
from models.user_model import UserModel

# Blueprint setup
auth_bp = Blueprint("auth", __name__)

def create_auth_routes(db):
    user_model = UserModel(db)

    @auth_bp.route("/signup", methods=["POST"])
    def signup():
        """API endpoint to register a new user."""
        data = request.get_json()

        # Extract data from request
        name = data.get("name")
        mobile = data.get("mobile")
        password = data.get("password")

        # Input validation
        if not (name and mobile and password):
            return jsonify({"error": "All fields are required"}), 400

        if not re.match(r"^[0-9]{10}$", mobile):
            return jsonify({"error": "Invalid mobile number"}), 400

        # Check for duplicate mobile number
        if user_model.is_mobile_registered(mobile):
            return jsonify({"error": "Mobile number already registered"}), 400

        # Create new user
        user_model.create_user(name, mobile, password)
        return jsonify({"message": "User registered successfully"}), 201

    return auth_bp
