from pymongo import MongoClient
from bson import ObjectId


class WishlistModel:
    def __init__(self, db):
        self.collection = db.wishlists  # Access the 'wishlists' collection
        self.products_collection = db.products  # Access the 'products' collection

    def add_product(self, data):
        """Add a product to the wishlist."""
        try:
            customer_id = data['customer_id']
            product_id = data['product_id']
            
            # Validate customer_id and product_id format
            if not ObjectId.is_valid(product_id):
                return {"message": "Invalid product_id format"}
            
            # Check if the product exists in the products collection
            product_details = self.products_collection.find_one({"_id": ObjectId(product_id)}, {"_id": 1, "name": 1, "price": 1, "category": 1})
            if not product_details:
                return {"message": "Product not found"}

            # Find the wishlist for the customer
            wishlist = self.collection.find_one({"customer_id": customer_id})
            
            if wishlist:
                # Add product to wishlist if it doesn't already exist
                if product_id not in [str(item) for item in wishlist['products']]:
                    self.collection.update_one(
                        {"customer_id": customer_id},
                        {"$push": {"products": ObjectId(product_id)}}  # Push product_id as ObjectId
                    )
                    return {"message": "Product added to wishlist"}
                else:
                    return {"message": "Product already in wishlist"}
            else:
                # Create a new wishlist if one doesn't exist for the customer
                self.collection.insert_one({
                    "customer_id": customer_id,
                    "products": [ObjectId(product_id)]  # Insert product_id as ObjectId
                })
                return {"message": "Product added to wishlist"}
        except Exception as e:
            print(f"Error adding product to wishlist: {e}")
            return {"message": "Error adding product to wishlist"}

    def get_wishlist_by_customer(self, customer_id):
        """Fetch the wishlist for a specific customer."""
        try:
            # Fetch wishlist for the customer
            wishlist = self.collection.find_one({"customer_id": customer_id})
            if wishlist:
                # Return product details along with product names
                product_ids = wishlist['products']
                products = []
                for product_id in product_ids:
                    product = self.products_collection.find_one({"_id": product_id}, {"_id": 0, "name": 1, "price": 1, "category": 1})
                    if product:
                        products.append(product)

                return {"customer_id": customer_id, "products": products}
            else:
                # Return empty wishlist if no wishlist exists
                return {"customer_id": customer_id, "products": []}
        except Exception as e:
            print(f"Error fetching wishlist: {e}")
            return {"message": "Error fetching wishlist"}

    def remove_product(self, data):
        """Remove a product from the wishlist."""
        try:
            customer_id = data['customer_id']
            product_id = data['product_id']
            
            # Validate product_id format
            if not ObjectId.is_valid(product_id):
                return {"message": "Invalid product_id format"}
            
            # Perform the remove operation
            result = self.collection.update_one(
                {"customer_id": customer_id},
                {"$pull": {"products": ObjectId(product_id)}}  # Pull product_id as ObjectId
            )

            if result.modified_count > 0:
                return {"message": "Product removed from wishlist"}
            else:
                return {"message": "Product not found in wishlist"}
        except Exception as e:
            print(f"Error removing product from wishlist: {e}")
            return {"message": "Error removing product from wishlist"}
