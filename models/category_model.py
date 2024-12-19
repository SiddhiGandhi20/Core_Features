from bson import ObjectId

class CategoryModel:
    def __init__(self, db):
        self.collection = db.categories  # Access the 'categories' collection

    def get_all_categories(self):
        """Fetch all categories from the collection."""
        try:
            categories = list(self.collection.find())  # Get all documents in the collection
            # Convert ObjectId to string for JSON serialization
            for category in categories:
                category["_id"] = str(category["_id"])  # Convert ObjectId to string
            return categories
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
        
    def get_category_by_name(self, name):
        """Fetch a category by its name."""
        try:
            category = self.collection.find_one({"name": name})
            if category:
                return category
            return None
        except Exception as e:
            print(f"Error fetching category: {e}")
            return None

    def get_category_by_id(self, category_id):
        """Fetch a single category by its ID."""
        try:
            category = self.collection.find_one({"_id": ObjectId(category_id)})
            if category:
                category["_id"] = str(category["_id"])  # Convert ObjectId to string
            return category
        except Exception as e:
            print(f"Error fetching category: {e}")
            return None

    def create_category(self, data):
        """Create a new category in the collection."""
        try:
            result = self.collection.insert_one(data)  # Insert the new category
            return str(result.inserted_id)  # Return the inserted ID as a string
        except Exception as e:
            print(f"Error creating category: {e}")
            return None

    def update_category(self, category_id, data):
        """Update an existing category by its ID."""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(category_id)}, {"$set": data}
            )
            return result.modified_count > 0  # Return True if update was successful
        except Exception as e:
            print(f"Error updating category: {e}")
            return False

    def delete_category(self, category_id):
        """Delete a category by its ID."""
        try:
            result = self.collection.delete_one({"_id": ObjectId(category_id)})
            return result.deleted_count > 0  # Return True if deletion was successful
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False
