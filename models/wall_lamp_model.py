from bson import ObjectId

class WallLampModel:
    def __init__(self, db):
        self.collection = db.wall_lamps  # Access the 'wall_lamps' collection

    def get_all_wall_lamps(self):
        """Fetch all wall lamps from the collection."""
        try:
            wall_lamps = list(self.collection.find())  # Get all documents in the collection
            # Convert ObjectId to string
            for lamp in wall_lamps:
                lamp["_id"] = str(lamp["_id"])  # Convert ObjectId to string for JSON serialization
            return wall_lamps
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
