from bson import ObjectId

class WallDecorModel:
    def __init__(self, db):
        self.collection = db.wall_decor  # Access the 'wall_decor' collection

    def get_all_wall_decor(self):
        """Fetch all wall decor items from the collection."""
        try:
            wall_decor_items = list(self.collection.find())  # Get all documents from the collection
            # Convert ObjectId to string for JSON serialization
            for item in wall_decor_items:
                item["_id"] = str(item["_id"])  # Convert ObjectId to string
            return wall_decor_items
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
