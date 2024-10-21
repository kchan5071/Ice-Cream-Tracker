from datetime import datetime, timedelta
from python_interface.database_connector import DatabaseWrapper


# check the inventory for available stock and get cost per item
def check_inventory(flavor, size, quantity):
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
    
# function to place order
def place_order(company, shipping_address, billing_address, line_items, shipping_method, customer_status):
    # default shipping cost (can change later)
    shipping_cost = 50

    total_cost = calculate_total(line_items, shipping_cost)
    
    # customer status limits
    if customer_status == "ok" and total_cost > 3000:
        print("Order exceeds the $3000 limit for 'OK' customers")
        return False
    elif customer_status == "shaky" and total_cost > 500:
        print("Order exceeds the $500 limit for 'SHAKY' customers")
        return False

    # insert order into order table
    order_date = datetime.now.strftime('%Y-%m-%d')
    #estimated arrival time is default 7 days from order date
    estimated_arrival = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    for item in line_items:
        flavor, size, quantity, _ = item
        is_available, item_cost = check_inventory(flavor, size, quantity)

        # insert order and update inventory if item is availiable
        if is_available:
            query = f"""
                INSERT INTO tracker.order (company, boxes, order_date, estimated_arrival, shipping_method, shipping_address, billing_address, subtotal_cost, shipping_cost, total_cost)
                VALUES ('{company}', {quantity}, '{order_date}', '{estimated_arrival}', '{shipping_method}', '{shipping_address}', '{billing_address}', {quantity * item_cost}, {shipping_cost}, {total_cost})
            """
            db_connector.send_query(query)

            #update inventory by decreasing available and increasing committed
            update_inventory_query = f"""
                UPDATE tracker."Inventory" SET available = available - {quantity}, committed = committed + {quantity}
                WHERE flavor = '{flavor}' AND size = '{size}'
            """
            db_connector.send_query(update_inventory_query)

        else:
            print(f"Insufficient stock for {flavor} - {size}.")
            return False
    
    print("Order placed successfully!")
    return True

def create_invoice():

def update_payment_status():

def cancel_order():

