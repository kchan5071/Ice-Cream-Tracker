from python_interface.database_connector import DatabaseWrapper
from inventory_management.InventoryManagement import InventoryManagement

def test_inventory_management():
    user = 'admin'
    password = 'password'
    host = 'localhost'
    port = '5432'
    database = 'icecreamtracker'
    schema = 'tracker'


    db = DatabaseWrapper(user, password, host, port, database, schema)
    db.connect()

    # Now create an instance of InventoryManagement
    inventory_manager = InventoryManagement(db)

    for i in range(99):
        inventory_manager.increment_available(1)

    #inventory_manager.update_defective(1)
    inventory_status = inventory_manager.get_inventory_status()

    if inventory_status:
        print("Inventory Status:")
        for item in inventory_status:
            print(f"ID: {item['id']}, Flavor: {item['flavor']}, Size: {item['size']}, Available: {item['available']}, Committed: {item['committed']}, Defective: {item['defective']}")
    else:
        print("No inventory data found or error fetching inventory.")
    # inventory_manager.add_product(2, 'Nut', 'L', 4.99, 50, 0, 0)

    db.close()

if __name__ == "__main__":
    test_inventory_management()


