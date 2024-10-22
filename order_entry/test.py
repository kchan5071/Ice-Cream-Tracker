import sys
import os

# Add the parent directory (Ice-Cream-Tracker) to sys.path so python_interface is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_interface.database_connector import DatabaseWrapper
from OrderEntry import place_order, create_invoice, check_order_table


def main():

    # if testing on computer ensure correct user (should match linux username)
    user = 'admin'
    password = 'password'
    host = 'localhost'
    port = '5432'
    database = 'icecreamtracker'
    schema = 'tracker'


    db_connector = DatabaseWrapper(user, password, host, port, database, schema)
    db_connector.connect()

    query = "SELECT * FROM tracker.inventory;"
    result = db_connector.send_query(query)
    
    if result:
        print("Inventory data:")
        for row in result:
            print(row)
    else:
        print("No data found in the Inventory table.")

    #test data for place_order
    company = "Ice Cream Co."
    shipping_address = "123 Frosty St."
    billing_address = "123 Frosty St."
    shipping_method = "Standard"
    customer_status = "ok" 

    # Example line items (flavor, size, quantity, item_cost)
    line_items = [
        ('vanilla', 'L', 10, 5.00),
        ('chocolate', 'M', 5, 3.00)
    ]

    check_order_table(db_connector)

    print("Testing place_order function...")
    result = place_order(db_connector, company, shipping_address, billing_address, line_items, shipping_method, customer_status)
    if result:
        print("Order placed successfully!")
    else:
        print("Order placement failed!")

    db_connector.close()

if __name__ == '__main__':
    main()