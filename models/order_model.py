from bson import ObjectId
from datetime import datetime

class OrderModel:
    def __init__(self, db):
        self.collection = db.orders  # Access the 'orders' collection

    def create_order(self, customer_id, product_id, quantity):
        """Create a new order in the collection."""
        try:
            data = {
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": quantity,
                "status": "pending",  # Default status is 'pending'
                "created_at": datetime.now(),
            }
            result = self.collection.insert_one(data)  # Insert the new order
            return str(result.inserted_id)  # Return the inserted ID as a string
        except Exception as e:
            print(f"Error creating order: {e}")
            return None

    def get_order_by_id(self, order_id):
        """Fetch an order by its ID."""
        try:
            order = self.collection.find_one({"_id": ObjectId(order_id)})
            if order:
                order["_id"] = str(order["_id"])  # Convert ObjectId to string for JSON serialization
            return order
        except Exception as e:
            print(f"Error fetching order: {e}")
            return None

    
    def update_order_status(self, order_id, status):
        """Update the status of an order."""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(order_id)}, {"$set": {"status": status}}
            )
            if result.modified_count > 0:
                # Return the updated order
                updated_order = self.collection.find_one({"_id": ObjectId(order_id)})
                updated_order["_id"] = str(updated_order["_id"])  # Convert ObjectId to string
                return updated_order
            return None
        except Exception as e:
            print(f"Error updating order status: {e}")
            return None

    def get_order_history(self, customer_id):
        """Fetch all orders for a customer."""
        try:
            orders = list(self.collection.find({"customer_id": customer_id}))
            for order in orders:
                order["_id"] = str(order["_id"])  # Convert ObjectId to string
            return orders
        except Exception as e:
            print(f"Error fetching order history: {e}")
            return None
