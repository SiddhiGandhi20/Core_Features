from flask import Blueprint, jsonify, request
from models.cart_model import CartModel
from models.wishlist_model import WishlistModel

cart_bp = Blueprint("cart", __name__)
wishlist_bp = Blueprint("wishlist", __name__)

def create_cart_routes(db):
    cart_model = CartModel(db)
    wishlist_model = WishlistModel(db)

    # Add product to cart
    @cart_bp.route("/cart/add", methods=["POST"])
    def add_to_cart():
        data = request.get_json()
        # Validate input data
        if not data.get("customer_id") or not data.get("product_id"):
            return jsonify({"message": "Missing customer_id or product_id"}), 400
        
        result = cart_model.add_product(data)
        if result:
            return jsonify({"message": result}), 200
        return jsonify({"message": "Error adding product to cart"}), 500

    # View cart
    @cart_bp.route("/cart", methods=["GET"])
    def view_cart():
        customer_id = request.args.get("customer_id")
        if not customer_id:
            return jsonify({"message": "Missing customer_id"}), 400
        
        cart = cart_model.get_cart_by_customer(customer_id)
        if cart:
            return jsonify(cart), 200
        return jsonify({"message": "Cart not found"}), 404

    # Update cart
    @cart_bp.route("/cart/update", methods=["PUT"])
    def update_cart():
        data = request.get_json()
        # Validate input data
        if not data.get("customer_id") or not data.get("product_id"):
            return jsonify({"message": "Missing customer_id or product_id"}), 400
        
        result = cart_model.update_cart(data)
        if result:
            return jsonify({"message": "Cart updated successfully"}), 200
        return jsonify({"message": "Error updating cart"}), 500

    # Remove product from cart
    @cart_bp.route("/cart/remove", methods=["DELETE"])
    def remove_from_cart():
        data = request.get_json()
        # Validate input data
        if not data.get("customer_id") or not data.get("product_id"):
            return jsonify({"message": "Missing customer_id or product_id"}), 400
        
        result = cart_model.remove_product(data)
        if result:
            return jsonify({"message": "Product removed from cart successfully"}), 200
        return jsonify({"message": "Error removing product from cart"}), 500

    # Add product to wishlist
    @wishlist_bp.route("/wishlist/add", methods=["POST"])
    def add_to_wishlist():
        data = request.get_json()

        # Validate input data
        required_fields = ["customer_id", "product_id", "name", "price", "category"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        result = wishlist_model.add_product(data)
        if result:
            return jsonify({"message": result}), 200
        return jsonify({"message": "Error adding product to wishlist"}), 500

    # View wishlist
    @wishlist_bp.route("/wishlist", methods=["GET"])
    def view_wishlist():
        customer_id = request.args.get("customer_id")
        
        # Validate input data
        if not customer_id:
            return jsonify({"message": "Missing customer_id"}), 400
        
        wishlist = wishlist_model.get_wishlist_by_customer(customer_id)
        if wishlist:
            return jsonify(wishlist), 200
        return jsonify({"message": "Wishlist not found"}), 404

    # Remove product from wishlist
    @wishlist_bp.route("/wishlist/remove", methods=["DELETE"])
    def remove_from_wishlist():
        data = request.get_json()

        # Validate input data
        if not data.get("customer_id") or not data.get("product_id"):
            return jsonify({"message": "Missing customer_id or product_id"}), 400

        result = wishlist_model.remove_product(data)
        if result:
            return jsonify({"message": "Product removed from wishlist"}), 200
        return jsonify({"message": "Error removing product from wishlist"}), 500

    return cart_bp, wishlist_bp
