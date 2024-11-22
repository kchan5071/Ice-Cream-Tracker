from datetime import datetime
from python_interface.database_connector import DatabaseWrapper

class InventoryManagement:
    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def add_product(self, id, flavor, size, cost, available, committed, defective):
        try:
            # Get the primary key column for the inventory table
            primary_key_column = self.db.get_primary_key("inventory")[0][0]

            # Check if the product already exists by searching the primary key
            existing_product = self.db.search_column("inventory", primary_key_column, id)

            if not existing_product:
                # If the product does not exist, insert it as a new product using __insert_row__
                new_data = (id, flavor, size, cost, available, committed, defective)
                self.db.__insert_row__("inventory", new_data)
                print(f"Added new product: ID: {id}, Flavor: {flavor}, Size: {size}, Cost: {cost}, Available: {available}, Committed: {committed}, Defective: {defective}")

        except Exception as e:
            print(f"Failed to add or update product: ID: {id}")
            print(e)
    
    def increment_available(self, id):
        # Get the primary key column for the inventory table
        primary_key_column = self.db.get_primary_key("inventory")[0][0]

        # Check if the product already exists by searching the primary key
        existing_product = self.db.search_column("inventory", primary_key_column, id)

        if existing_product:
            current_available = existing_product[0][4]  # Assuming 'available' is the 5th column
            
            # Increment the available count
            new_available = current_available + 1

            # Update the available column
            self.db.update_from_primary_key("inventory", id, 'available', new_available)
            self.db.connection.commit()
            print(f"Updated product: ID: {id}, 'available': {new_available}")

    def decrement_available(self, id):
        # Get the primary key column for the inventory table
        primary_key_column = self.db.get_primary_key("inventory")[0][0]

        # Check if the product already exists by searching the primary key
        existing_product = self.db.search_column("inventory", primary_key_column, id)

        if existing_product:
            current_available = existing_product[0][4]  # Assuming 'available' is the 5th column
            
            # Increment the available count
            new_available = current_available - 1

            # Update the available column
            self.db.update_from_primary_key("inventory", id, 'available', new_available)
            self.db.connection.commit()
            print(f"Updated product: ID: {id}, 'available': {new_available}")
    
    def update_commited(self, id):
        # Get the primary key column for the inventory table
        primary_key_column = self.db.get_primary_key("inventory")[0][0]

        # Check if the product already exists by searching the primary key
        existing_product = self.db.search_column("inventory", primary_key_column, id)

        if existing_product:
            current_available = existing_product[0][4]  # Assuming 'available' is the 5th column
            current_committed = existing_product[0][5]  # Assuming 'available' is the 6th column
            
            if (current_available <= 0):
                print("None available")
                return None
            
            new_available = current_available - 1
            new_committed = current_committed + 1

            # Update the available and committ column
            self.db.update_from_primary_key("inventory", id, 'available', new_available)
            self.db.update_from_primary_key("inventory", id, 'committed', new_committed)
            self.db.connection.commit()
            print(f"Updated product: ID: {id}, 'available': {new_available}, 'committed': {new_committed}")

    def update_defective(self, id):
        # Get the primary key column for the inventory table
        primary_key_column = self.db.get_primary_key("inventory")[0][0]

        # Check if the product already exists by searching the primary key
        existing_product = self.db.search_column("inventory", primary_key_column, id)

        if existing_product:
            current_defective = existing_product[0][6]  # Assuming 'available' is the 7th column
            
            # Increment the available count
            new_defective = current_defective + 1

            # Update the available column
            self.db.update_from_primary_key("inventory", id, 'defective', new_defective)
            self.db.connection.commit()
            print(f"Updated product: ID: {id}, 'defective': {new_defective}")

    def remove_product(self, id):
        try:
            # Check if the product exists
            existing_product = self.db.search_column('inventory', 'id', id)
            
            if existing_product:
                # If the product exists, delete it
                deleted_id = self.db.delete_row('inventory', 'id', id)
                if deleted_id:
                    print(f"Product with ID: {id} has been removed successfully.")
                else:
                    print(f"Failed to remove product with ID: {id}.")
            else:
                print(f"Product with ID: {id} does not exist.")

        except Exception as e:
            print(f"Error in remove_product: {e}")

    def get_inventory_status(self):
        try:
            # Fetch all rows from the inventory table using the existing fetch_all method
            result = self.db.fetch_all("inventory")
            
            if result:
                # Prepare a list of dictionaries showing available and committed quantities
                inventory_status = []
                for row in result:
                    id, flavor, size, available, committed, defective = row[0], row[1], row[2], row[4], row[5], row[6]  # assuming column order
                    inventory_status.append({
                        "id": id,
                        "flavor": flavor,
                        "size": size,
                        "available": available,
                        "committed": committed,
                        "defective": defective
                    })
                return inventory_status
            else:
                print("No inventory data found.")
                return None
        except Exception as e:
            print(f"Error fetching inventory status: {e}")
            return None




