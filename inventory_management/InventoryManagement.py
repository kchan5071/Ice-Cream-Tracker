from datetime import datetime
from python_interface.database_connector import DatabaseWrapper

class InventoryManagement:
    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def add_product(self, id, flavor, size, cost, available, committed, defective):
        # Check if the product already exists
        existing_product = self.db.search_column('inventory', 'id', id)

        if existing_product:
            print(f"Product with ID {id} already exists. Updating values.")
            # If the product exists, we will update the relevant fields
            update_data = (flavor, size, cost, available, committed, defective, id)
            update_query = f"""
            UPDATE {self.db.schema}.inventory
            SET flavor = %s,
                size = %s,
                cost = %s,
                available = %s,
                committed = %s,
                defective = %s
            WHERE id = %s
            """
            self.db.cursor.execute(update_query, update_data)
            self.db.connection.commit()
            print(f"Updated product: ID: {id}, Flavor: {flavor}, Size: {size}, Cost: {cost}, Available: {available}, Committed: {committed}, Defective: {defective}")
        else:
            # If the product does not exist, insert it as a new product
            new_data = (id, flavor, size, cost, available, committed, defective)
            
            # Change this line to use the proper insertion logic
            insert_query = f"""
            INSERT INTO {self.db.schema}.inventory (id, flavor, size, cost, available, committed, defective)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            self.db.cursor.execute(insert_query, new_data)
            self.db.connection.commit()
            print(f"Added new product: ID: {id}, Flavor: {flavor}, Size: {size}, Cost: {cost}, Available: {available}, Committed: {committed}, Defective: {defective}")

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
            query = f"SELECT flavor, size, available, committed FROM {self.db.schema}.inventory;"
            result = self.db.send_query(query)
            
            if result:
                # Prepare a list of dictionaries showing available and committed quantities
                inventory_status = []
                for row in result:
                    flavor, size, available, committed = row
                    inventory_status.append({
                        "flavor": flavor,
                        "size": size,
                        "available": available,
                        "committed": committed
                    })
                return inventory_status
            else:
                print("No inventory data found.")
                return None
        except Exception as e:
            print(f"Error fetching inventory status: {e}")
            return None

# def log_transaction(self, user, transaction_type, inventory_id, reason=None):

# def move_inventory_out(self, inventory_id, disposition, order_id=None):

# def create_ticket(self, disposition, inventory_id):

# def generate_report(self, period="month"):




