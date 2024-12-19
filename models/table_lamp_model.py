from bson import ObjectId

class TableLampModel:
    def __init__(self, db):
        self.collection = db.table_lamps  # Access the 'table_lamps' collection

    def get_all_table_lamps(self):
        """Fetch all table lamps from the collection."""
        try:
            table_lamps = list(self.collection.find())  # Get all documents in the collection
            # Convert ObjectId to string
            for lamp in table_lamps:
                lamp["_id"] = str(lamp["_id"])  # Convert ObjectId to string for JSON serialization
            return table_lamps
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
