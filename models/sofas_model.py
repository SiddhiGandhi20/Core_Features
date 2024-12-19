from bson import ObjectId

class SofaModel:
    def __init__(self, db):
        self.collection = db.sofas  # Access the 'sofas' collection

    def get_all_sofas(self):
        """Fetch all sofas from the collection."""
        try:
            sofas = list(self.collection.find())  # Get all documents in the collection
            # Convert ObjectId to string
            for sofa in sofas:
                sofa["_id"] = str(sofa["_id"])  # Convert ObjectId to string for JSON serialization
            return sofas
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
