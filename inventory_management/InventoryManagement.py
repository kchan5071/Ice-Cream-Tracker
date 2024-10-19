from datetime import datetime

class InventoryManagement:
    def __init__(self, db_wrapper):
        self.db = db_wrapper
        self.db.connect()

    def check_connection(self):
        # Check if the connection to the database is active
        try:
            self.db.cursor.execute("SELECT 1;")  # A simple query to check connection
            return True
        except Exception as e:
            print("Connection check failed:", e)
            return False

    def add_product(self, flavor, size, cost=5.00, available=0, committed=0, defective=0):
        try:
            # Prepare the data for insertion as a tuple
            data = (flavor, size, cost, available, committed, defective)

            # Fetch column names for the Inventory table
            if self.db.columns is None or self.db.get_table_index("tracker.Inventory") is None:
                print("Fetching column names for Inventory table.")
                self.db.fetch_column_names("tracker.Inventory")

            # Use the DatabaseWrapper's insert_data method
            inserted_data = self.db.insert_data("tracker.Inventory", data)
            if inserted_data is not None:
                print(f"Added new product: Flavor: {flavor}, Size: {size}, Cost: {cost}, Available: {available}, Committed: {committed}, Defective: {defective}")
            else:
                print("Failed to add product.")
        except Exception as e:
            print(f"Error adding product: {e}")


