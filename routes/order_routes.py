from flask import Blueprint, jsonify, request
from models.order_model import OrderModel

# Define the Blueprint for order routes
order_bp = Blueprint("order", __name__)

def create_order_routes(db):
    order_model = OrderModel(db)

    # Create Order (POST)
    @order_bp.route("/orders", methods=["POST"])
    def create_order():
        """Create a new order."""
        data = request.get_json()
        
        customer_id = data.get("customer_id")  # Get customer_id from request
        product_id = data.get("product_id")  # Get product_id from request
        quantity = data.get("quantity")  # Get quantity from request
        
        if not customer_id or not product_id or not quantity:
            return jsonify({"message": "customer_id, product_id, and quantity are required"}), 400

        order_id = order_model.create_order(customer_id, product_id, quantity)
        if order_id:
            return jsonify({"message": "Order created successfully", "order_id": order_id}), 201
        return jsonify({"message": "Error creating order"}), 500

    # Get Order (GET by order_id)
    @order_bp.route("/orders/<order_id>", methods=["GET"])
    def get_order(order_id):
        """Fetch an order by its ID."""
        order = order_model.get_order_by_id(order_id)
        if not order:
            return jsonify({"message": "Order not found"}), 404
        return jsonify(order), 200

    # Get Order History (GET by customer_id)
    @order_bp.route("/orders/history/<customer_id>", methods=["GET"])
    def get_order_history(customer_id):
        """Fetch all orders for a specific customer."""
        orders = order_model.get_order_history(customer_id)
        if not orders:
            return jsonify({"message": "No orders found for this customer"}), 404
        return jsonify(orders), 200

    # Update Order Status (PUT)
    @order_bp.route("/orders/<order_id>/status", methods=["PUT"])
    def update_order_status(order_id):
        """Update the status of an existing order."""
        try:
            # Get the new status from the request data
            data = request.get_json()
            if not data or "status" not in data:
                return jsonify({"message": "Status is required"}), 400
            
            # Fetch the order and update its status
            order = order_model.get_order_by_id(order_id)
            if not order:
                return jsonify({"message": "Order not found"}), 404
            
            # Update the order status
            updated_order = order_model.update_order_status(order_id, data["status"])
            if updated_order:
                return jsonify({"message": "Order status updated successfully", "order": updated_order}), 200
            return jsonify({"message": "Error updating order status"}), 500

        except Exception as e:
            print(f"Error updating order status: {e}")
            return jsonify({"message": f"Error updating order status: {str(e)}"}), 500

    return order_bp
