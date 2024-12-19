from bson import ObjectId

class BedsModel:
    def __init__(self, db):
        self.collection = db.beds  # The collection name is 'beds'

    def get_all_beds(self):
        """Fetch all beds records from the collection."""
        try:
            beds = list(self.collection.find())
            # Convert ObjectId to string
            for bed in beds:
                bed["_id"] = str(bed["_id"])  # Convert ObjectId to string
            return beds
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
