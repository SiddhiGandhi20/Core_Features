from flask import Blueprint, request, jsonify
from models.signin_model import SignInModel
import uuid  # Import uuid for unique ID generation

# Blueprint setup
signin_bp = Blueprint("signin", __name__)

def create_signin_routes(db):
    signin_model = SignInModel(db)

    @signin_bp.route("/signin", methods=["POST"])
    def signin():
        """
        API Endpoint for user sign-in.
        Accepts mobile number and password.
        """
        data = request.get_json()

        # Extract fields
        mobile = data.get("mobile")
        password = data.get("password")

        # Input validation
        if not (mobile and password):
            return jsonify({"error": "Mobile number and password are required"}), 400

        # Check user credentials
        user = signin_model.validate_user(mobile, password)
        if not user:
            return jsonify({"error": "Invalid mobile number or password"}), 401

        # Generate customer ID (UUID)
        customer_id = str(uuid.uuid4())  # Generate a unique customer ID

        # Store customer ID in the login collection
        db.login.update_one(
            {"mobile": mobile},  # Find the user by mobile number
            {"$set": {"customer_id": customer_id}},  # Set the generated customer_id
            upsert=True  # If the user doesn't exist, create a new document
        )

        # Success response (excluding password)
        return jsonify({
            "message": "Login successful",
            "user": {
                "name": user["name"],
                "mobile": user["mobile"],
                "customer_id": customer_id  # Include the generated customer ID
            }
        }), 200

    return signin_bp
