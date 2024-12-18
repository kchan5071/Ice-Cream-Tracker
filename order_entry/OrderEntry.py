from datetime import datetime, timedelta
from python_interface.database_connector import DatabaseWrapper
from decimal import Decimal

#get inventory id from flavor and size in order to update the values
def get_inventory_id(db_connector, flavor, size):
    query = f"SELECT id FROM tracker.inventory WHERE flavor = '{flavor}' AND size = '{size}'"
    result = db_connector.send_query(query)
    return result[0][0] if result else None

# empty the order table
def clear_order_table(db_connector):
    try:
        query = "DELETE FROM tracker.order;"
        db_connector.send_query(query)
        print("Order table cleared successfully.")
    except Exception as e:
        print("Error clearing the order table.")
        print(e)

# view order table
def check_order_table(db_connector):
    # Query to fetch all records from the order table
    query = "SELECT * FROM tracker.order;"
    # Execute the query and fetch the results
    result = db_connector.send_query(query)
    if result:
        print("Order data:")
        for row in result:
            print(row)
    else:
        print("No data found in the Order table.")

# check the inventory for available stock and get cost per item
def check_inventory(db_connector, flavor, size, quantity):
    query = f"""
        SELECT available, cost FROM tracker.inventory
        WHERE flavor = '{flavor}' AND size = '{size}'
    """
    result = db_connector.send_query(query)
    
    if result and result[0][0] >= quantity:
        available_quantity = result[0][0]
        item_cost = result[0][1]
        return True, item_cost
    else:
        return False, 0
    
# calculate total cost, including shipping cost
# line item example: ("Vanilla", "Large", 10, 5.00)
def calculate_total(line_items, shipping_cost):
    total_cost = 0
    total_cost += shipping_cost
    for item in line_items:
        flavor, size, quantity, item_cost = item
        total_cost += quantity * item_cost
    return total_cost

def get_next_order_id(db_connector):
    query = "SELECT COALESCE(MAX(id), 0) + 1 FROM tracker.order;"
    result = db_connector.send_query(query)
    return result[0][0] if result else 1

#validate the input types of the order entry
def validate_order_values(order_values):
    expected_types = [
        int,    # id
        str,    # company
        int,    # boxes (quantity)
        str,    # order_date
        str,    # estimated_arrival
        str,    # arrival (hardcoded)
        str,    # shipping_method
        str,    # shipping_address
        str,    # billing_address
        str,    # shipping_status (hardcoded)
        Decimal,  # subtotal_cost
        Decimal,  # shipping_cost
        Decimal,  # total_cost
        str     # payment_date (hardcoded)
    ]

    for value, expected_type in zip(order_values, expected_types):
        if not isinstance(value, expected_type):
            raise ValueError(
                f"Invalid type for value '{value}'. "
                f"Expected {expected_type.__name__}, got {type(value).__name__}."
            )
    
# function to place order
def place_order(db_connector, company, shipping_address, billing_address, line_items, shipping_method, customer_status):
    
    # default shipping cost (can change later)
    shipping_cost = 50

    total_cost = calculate_total(line_items, shipping_cost)
    
    # customer status limits
    if customer_status == "ok" and total_cost > 3000:
        print("Order exceeds the $3000 limit for 'OK' customers")
        return "Order exceeds the $3000 limit for 'OK' customers"
    elif customer_status == "shaky" and total_cost > 500:
        print("Order exceeds the $500 limit for 'SHAKY' customers")
        return "Order exceeds the $500 limit for 'SHAKY' customers"

    # insert order into order table
    order_date = datetime.now().strftime('%Y-%m-%d')
    #estimated arrival time is default 7 days from order date
    estimated_arrival = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    for item in line_items:
        flavor, size, quantity, _ = item
        is_available, item_cost = check_inventory(db_connector, flavor, size, quantity)
        order_id = get_next_order_id(db_connector)
        print(order_id)
        
        # insert order and update inventory if item is availiable
        if is_available:

            # Build the row for the order table
            order_values = [
                order_id,                # id
                company,                 # company
                quantity,                # boxes
                order_date,              # order_date
                estimated_arrival,        # estimated_arrival
                '2055-01-01',                    # arrival (not known at order time) (hardcode date)
                shipping_method,          # shipping_method
                shipping_address,         # shipping_address
                billing_address,          # billing_address
                'In Transit',                    # shipping_status (not set initially) (hardcode)
                quantity * item_cost,     # subtotal_cost
                Decimal(shipping_cost),            # shipping_cost
                Decimal(total_cost),               # total_cost
                '2055-01-01'                     # payment_date (not known at order time) (hardcode)
            ]

            print("Order values: ")
            print(order_values)

            try:
                validate_order_values(order_values)
            except ValueError as e:
                print(f"Type validation error: {e}")
                return f"Type validation error: {e}"

            # Use __insert_row__ to insert the row
            db_connector.__insert_row__('order', order_values)

            #update inventory by decreasing available and increasing committed
            inventory_id = get_inventory_id(db_connector, flavor, size)

            if inventory_id:
                # Use the id for updating available and committed stock

                # retrieve current available and committed values
                query = f"SELECT available, committed FROM tracker.inventory WHERE id = {inventory_id}"
                result = db_connector.send_query(query)

                if result:
                    curr_available = result[0][0]
                    curr_committed = result[0][1]
                    new_available = curr_available - quantity
                    new_committed = curr_committed + quantity
                    db_connector.update_from_primary_key('inventory', inventory_id, 'available', new_available)
                    db_connector.update_from_primary_key('inventory', inventory_id, 'committed', new_committed)
            else:
                print(f"Error: Could not find inventory item for {flavor} - {size}")
                return f"Error: Could not find inventory item for {flavor} - {size}"

        else:
            print(f"Insufficient stock for {flavor} - {size}.")
            return f"Insufficient stock for {flavor} - {size}."
    
    print("Order placed successfully!")
    return "Order placed successfully!"

def create_invoice(db_connector, order_id):
    query = f"""
        SELECT * FROM tracker.order WHERE id = {order_id}
    """
    result = db_connector.send_query(query)
    if result:
        print("Invoice for Order Id:", order_id)
        print(result) #change format later
    else:
        print("Order not found.")


def update_payment_status(db_conenctor, order_id, new_status):
    try:
        db_conenctor.update_row('order', 'payment_status', new_status, order_id)
        print(f"Payment status and date updated successfully for Order ID: {order_id}.")
        return True
    except Exception as e:
        print(f"Error updating payment status for Order ID: {order_id}.")
        print(e)
        return False

