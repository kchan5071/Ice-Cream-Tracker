import sys
import os

# Add the parent directory (Ice-Cream-Tracker) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_interface.database_connector import DatabaseWrapper


#operations to do on shipments
class ShipmentSystem:
    def __init__(self, user, password, host, port, database, schema):
        self.db = DatabaseWrapper(user, password, host, port, database, schema)
        self.db.connect()
    
    #adding shipment info to an order by id
    def add_shipment_info(self,id, company, boxes, order_date, estimated_arrival, arrival, full_or_partial, shipment_method_id):
        data = {
            'id': id,
            'company': company,
            'boxes': boxes,
            'order_date': order_date,
            'estimated_arrival': estimated_arrival,
            'arrival': arrival,
            'full_or_partial': full_or_partial, # True for full, False for partial
            'shipment_method_id': shipment_method_id
        }
        #if no order w id exists, add it
        if not self.row_exists('order', id):
            self.insert_order_row(id, company, boxes, order_date, estimated_arrival, arrival, full_or_partial)
        else:
            #adding shipment info if row exists
            for column, value in data.items():
                if value is not None:
                    self.db.update_from_primary_key('order',id, column, value)   
        print(f"Shipment info for order ID {id} added successfully!")
        
    #getting shipment info
    def get_shipment_info(self, id):
        query = "SELECT id, boxes, order_date, estimated_arrival, arrival, full_or_partial FROM tracker.Order WHERE id = %s;"
        self.db.cursor.execute(query, (id,))
        row = self.db.cursor.fetchone()
        
        if row:
            id, boxes, shipment_date, estimated_arrival, arrival, full_or_partial = row
            return {
                'Order ID': id,
                'Date Shipped': format_date(shipment_date),
                'Shipment Boxes': boxes,
                'Full/Partial Shipment': 'Full' if full_or_partial else 'Partial',
                'Estimated Arrival': format_date(estimated_arrival),
                'Arrrival Date': format_date(arrival),
                'Status': 'Delivered' if arrival else 'In Transit',
            }
        else:
            return None
    
    
    #updating shipment arrival date
    def update_shipment_info(self, id, new_arrival = None):
        try:
            updates = []
            params = []
        
            if new_arrival is not None:
                updates.append("arrival = %s")
                params.append(new_arrival)
        
            params.append(id)
        
            if updates:
                query = f"UPDATE tracker.Order SET {', '.join(updates)} WHERE id = %s;"
                self.db.cursor.execute(query, params)
                self.db.connection.commit()
                print(f"Shipment {id} updated successfully!")
            else:
                print("No changes to update.")
        except Exception as e:
            print(f"Error updating shipment {id}: {e}")
            
    def insert_order_row(self, id, company, boxes, order_date, estimated_arrival, arrival, full_or_partial):
        query = """
        INSERT INTO tracker.order (id, company, boxes, order_date, estimated_arrival, arrival, full_or_partial)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        try:
            self.db.cursor.execute(query, (id, company, boxes, order_date, estimated_arrival, arrival, full_or_partial))
            self.db.connection.commit()
        except Exception as e:
            print(f"Error inserting row into order table: {e}")

    def row_exists(self, table, id):
        query = f"SELECT 1 FROM tracker.{table} WHERE id = %s;"
        try:
            self.db.cursor.execute(query, (id,))
            return self.db.cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking if row exists: {e}")
            return False
    
    #shipment report
    def shipment_report(self):
        query = "SELECT * FROM tracker.order WHERE order_date IS NOT NULL AND arrival IS NULL;"
        self.db.cursor.execute(query)
        row = self.db.cursor.fetchall()
        print("Active orders ready for shipment report:")
        for r in row:
            print(f"ID: {r[0]}, Company: {r[1]}, Boxes: {r[2]}, Order Date: {r[3]}, Estimated Arrival: {r[4]}, Arrival:{r[5]}, Full/Partial: {'Full' if r[6] else 'Partial'}")



    #user function to query shipments based on name, order date, or expected arrival date
    def query_shipments(self, company = None, order_date = None, estimated_arrival = None):
        query = "SELECT * FROM tracker.order WHERE 1=1"
        params = []
        
        if company is not None:
            query += " AND company = %s"
            params.append(company)
        if order_date is not None:
            query += " AND order_date = %s"
            params.append(order_date)
        if estimated_arrival is not None:
            query += " AND estimated_arrival = %s"
            params.append(estimated_arrival)
            
        self.db.cursor.execute(query, params)
        rows = self.db.cursor.fetchall()
        if rows:
            return rows
        else:
            print("No matching orders found.")
    
    
    #function to cancel/modify order
    def cancel_order(self, id):
        query = f"""
        SELECT id, shipping_cost FROM tracker.Order 
        WHERE id = %s AND shipping_status IN ('In Transit');
        """
        self.db.cursor.execute(query, (id,))
        row = self.db.cursor.fetchone()
        total_cost = sum(r[1] for r in row)
        
        update_query = f"""
        UPDATE shipments
        SET shipping_status = 'canceled'
        WHERE id = {id} AND status IN ('In Transit');
        """
        self.db.cursor.execute(query, (id,))
        print(f"Order {id} canceled successfully. Customer will still be billed: ${total_cost}")
    
    ###### ADMIN FUNCTIONS FOR SHIPPINH METHODS ######
    
    #function to add shipment methods 
    def add_shipment_method(self, method_name, region):
        try:
            query = """
            INSERT INTO tracker.ShipmentMethods (method_name, region)
            VALUES (%s, %s);
            """
            self.db.cursor.execute(query, (method_name, region))
            self.db.connection.commit()
            print(f"Shipment method '{method_name}' for region '{region}' added successfully!")
        except Exception as e:
            print(f"Error adding shipment method: {e}")
    
    #updating existing shipment method
    def update_shipment_method(self, order_id, method_id):
        query = """
        UPDATE tracker.order 
        SET shipment_method_id = %s 
        WHERE id = %s;
        """
        params = (method_id, order_id)

        try:
         # Execute the query with the given parameters
            self.db.cursor.execute(query, params)
            self.db.connection.commit()
            print(f"Order {order_id} updated to use shipment method ID {method_id} successfully!")
        except Exception as e:
            print(f"Error updating shipment method for order ID {order_id}: {e}")
        
        
        
    #getting shipment method for desired region
    def get_methods_for_region(self, region):
        try:
            query = "SELECT id, method_name FROM tracker.ShipmentMethods WHERE region = %s;"
            self.db.cursor.execute(query, (region,))
            methods = self.db.cursor.fetchall()
            if methods:
                print(f"Available shipment methods for {region}:")
                for method in methods:
                    print(f"{method[1]}")
            else:
                print(f"No shipment methods available for region {region}")
        except Exception as e:
            print(f"Error retrieving shipment methods: {e}")

    #getting shipment method info by order id
    def get_shipment_method_info(self, id):
        info = self.get_shipment_info(id)
        
        query = """
        SELECT s.method_name AS "Shipment Method", s.region AS "Shipment Region"
        FROM tracker.ShipmentMethods s
        JOIN tracker.order o ON o.shipment_method_id = s.id
        WHERE o.id = %s;"""
        self.db.cursor.execute(query, (id,))
        row = self.db.cursor.fetchone()
        if row:
            print("Order Details with Shipment Method:")
            info.update({
                'Method': row[0],
                'Region': row[1]
            })
            return print(info)
        else:
            print(f"No order found with ID {id}")
            return None



    #deleting shipment method 
    def delete_shipment_method(self, method_id):
        try:
            query = "DELETE FROM tracker.ShipmentMethods WHERE id = %s;"
            self.db.cursor.execute(query, (method_id,))
            self.db.connection.commit()
            print(f"Shipment method {method_id} deleted successfully!")
        except Exception as e:
            print(f"Error deleting shipment method: {e}")
            
    #function to add vendor to list by admin
    def add_vendor(self,name, type, region, rate, rank):
        try:
            query = """
            INSERT INTO tracker.Shipment_vendors (name, type, region, rate, rank)
            VALUES (%s, %s, %s, %s, %s);
            """
            self.db.cursor.execute(query, (name, type, region, rate, rank))
            self.db.connection.commit()
            print(f"Vendor '{name}' added successfully!")
        except Exception as e:
            print(f"Error adding vendor: {e}")
            
    #updating any  vendor info by name
    def update_vendor(self, name = None, type = None, region = None, rate = None, rank = None):
        query = """UPDATE shippind_vendors SET """
        updates = []
        if name is not None:
            updates.append("name = %s")
        if type is not None:
            updates.append("type = %s")
        if region is not None:
            updates.append("region = %s")
        if rate is not None:
            updates.append("rate = %s")
        if rank is not None:
            updates.append("rank = %s")
        query += ", ".join(updates) + " WHERE name = %s;"
        self.db.cursor.execute(query, (name, type, region, rate, rank))
        self.db.connection.commit()
        print(f"Vendor {name} updated successfully!")
        
    #deleting vendor by name
    def delete_vendor(self, name):
        try:
            query = "DELETE FROM tracker.Shipment_vendors WHERE name = %s;"
            self.db.cursor.execute(query, (name,))
            self.db.connection.commit()
            print(f"Vendor {name} deleted successfully!")
        except Exception as e:
            print(f"Error deleting vendor: {e}")

    #clearing table
    def clear_table(self, table):
        self.db.cursor.execute(f"TRUNCATE TABLE tracker.{table} RESTART IDENTITY CASCADE;")
        self.db.clear_table(table)
        
    def close(self):
        self.db.close()
    
    
#formatting date
def format_date(date_obj):
    return date_obj.strftime('%Y-%m-%d') if date_obj else None
