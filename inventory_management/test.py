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


    db.close()

if __name__ == "__main__":
    test_inventory_management()


