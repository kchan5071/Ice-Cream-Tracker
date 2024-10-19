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

    # Query to fetch table names in 'tracker' schema
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'tracker';"
    tables = db.send_query(query)
    print(f"Tables in 'tracker' schema: {tables}")
    print(db.search_column('customer','password','chicken'))
    
    db.close()


if __name__ == "__main__":
    test_inventory_management()


