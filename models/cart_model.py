from bson import ObjectId

# Helper function to convert ObjectId to string
def convert_objectid(data):
    if isinstance(data, dict):
        return {key: convert_objectid(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

class CartModel:
    
    def __init__(self, db):
        self.collection = db.carts  # Access the 'carts' collection

    def add_product(self, data):
        """Add a product to the cart."""
        try:
            customer_id = data['customer_id']
            if not customer_id:
                raise ValueError("customer_id is required")

            product = {
                "product_id": data['product_id'],
                "name": data['name'],
                "price": data['price'],
                "category": data['category'],
                "quantity": data['quantity']
            }

            # Find the cart for the customer
            cart = self.collection.find_one({"customer_id": customer_id})

            if cart:
                # Check if the product already exists in the cart and update it
                existing_product = next((item for item in cart['products'] if item['product_id'] == product['product_id']), None)
                if existing_product:
                    # Increment quantity if product already exists
                    self.collection.update_one(
                        {"customer_id": customer_id, "products.product_id": product['product_id']},
                        {"$inc": {"products.$.quantity": product['quantity']}}  # Increment quantity
                    )
                else:
                    # Add the product to the cart
                    self.collection.update_one(
                        {"customer_id": customer_id},
                        {"$push": {"products": product}}
                    )
            else:
                # Create a new cart if none exists for the customer
                self.collection.insert_one({
                    "customer_id": customer_id,
                    "products": [product]
                })

            return "Product added to cart"
        except ValueError as e:
            print(f"Error: {e}")
            return {"message": str(e)}
        except Exception as e:
            print(f"Error adding product to cart: {e}")
            return {"message": "Error adding product to cart"}

    def get_cart_by_customer(self, customer_id):
        """Fetch the cart for a specific customer."""
        try:
            if not customer_id:
                raise ValueError("customer_id is required")

            cart = self.collection.find_one({"customer_id": customer_id})
            if not cart:
                return {"message": "Cart not found for the customer"}
            
            return convert_objectid(cart)  # Convert ObjectId to string
        except ValueError as e:
            print(f"Error: {e}")
            return {"message": str(e)}
        except Exception as e:
            print(f"Error fetching cart: {e}")
            return {"message": "Error fetching cart"}

    def update_cart(self, data):
        """Update the cart for a specific customer."""
        try:
            customer_id = data['customer_id']
            product_id = data['product_id']
            quantity = data['quantity']

            if not customer_id or not product_id or quantity is None:
                raise ValueError("Missing required fields: customer_id, product_id, or quantity")

            # Update the product quantity in the cart
            result = self.collection.update_one(
                {"customer_id": customer_id, "products.product_id": product_id},
                {"$set": {"products.$.quantity": quantity}}
            )

            if result.modified_count == 0:
                return {"message": "No product updated"}
            
            return {"message": "Cart updated successfully"}
        except ValueError as e:
            print(f"Error: {e}")
            return {"message": str(e)}
        except Exception as e:
            print(f"Error updating cart: {e}")
            return {"message": "Error updating cart"}

    def remove_product(self, data):
        """Remove a product from the cart."""
        try:
            customer_id = data['customer_id']
            product_id = data['product_id']

            if not customer_id or not product_id:
                raise ValueError("Missing required fields: customer_id or product_id")

            result = self.collection.update_one(
                {"customer_id": customer_id},
                {"$pull": {"products": {"product_id": product_id}}}
            )

            if result.modified_count == 0:
                return {"message": "Product not found in cart"}
            
            return {"message": "Product removed from cart"}
        except ValueError as e:
            print(f"Error: {e}")
            return {"message": str(e)}
        except Exception as e:
            print(f"Error removing product from cart: {e}")
            return {"message": "Error removing product from cart"}
