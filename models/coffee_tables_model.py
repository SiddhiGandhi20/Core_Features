from bson import ObjectId

class CoffeeTableModel:
    def __init__(self, db):
        self.collection = db.coffee_tables  # Access the 'coffee_tables' collection

    def get_all_coffee_tables(self):
        """Fetch all coffee tables from the collection."""
        try:
            coffee_tables = list(self.collection.find())  # Get all documents in the collection
            # Convert ObjectId to string
            for table in coffee_tables:
                table["_id"] = str(table["_id"])  # Convert ObjectId to string for JSON serialization
            return coffee_tables
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
