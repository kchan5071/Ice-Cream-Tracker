import sys
import os

# Add the parent directory (Ice-Cream-Tracker) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_interface.database_connector import DatabaseWrapper

#shipment structure
class Shipments:
    def __init__(self, id, boxes, shipment_date, estimated_arrival, arrival, full_or_partial):
        self.id = id
        self.boxes = boxes
        self.shipment_date = shipment_date
        self.estimated_arrival = estimated_arrival
        self.arrival = arrival
        self.full_or_partial = full_or_partial #True for full, False for partial
        

#operations to do on shipments
class ShipmentSystem:
    def __init__(self, user, password, host, port, database, schema):
        self.db = DatabaseWrapper(user, password, host, port, database, schema)
        self.db.connect()
    
    #adding shipment info
    def add_shipment_info(self,id, boxes, order_date, estimated_arrival, arrival, full_or_partial, company):
        query = """
        INSERT INTO tracker.Order (id, boxes, order_date, estimated_arrival, arrival, full_or_partial, company)
        VALUES (%s, %s, %s, %s, %s, %s,%s);
        """
        self.db.cursor.execute(query, (id, boxes, order_date, estimated_arrival, arrival, full_or_partial, company))
        self.db.connection.commit()
        print(f"Shipment with ID {id} added successfully!")
        
    #getting shipment info
    def get_shipment_info(self, id):
        query = "SELECT id, boxes, order_date, estimated_arrival, arrival, full_or_partial FROM tracker.Order WHERE id = %s;"
        self.db.cursor.execute(query, (id,))
        row = self.db.cursor.fetchone()
        
        if row:
            id, boxes, shipment_date, estimated_arrival, arrival, full_or_partial = row
            return {
                'Order ID': id,
                'Date Shipped': shipment_date,
                'Shipment Boxes': boxes,
                'Full/Partial Shipment': 'Full' if full_or_partial else 'Partial',
                'estimated arrival': estimated_arrival,
                'Arrrival Date': arrival,
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
            
    
    #function to add shipment methods by admin
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
    
    #this function is used to get shipment methods for a particular region
    def get_methods_for_region(self, region):
        try:
            query = "SELECT id, method_name FROM tracker.ShipmentMethods WHERE region = %s;"
            self.db.cursor.execute(query, (region,))
            methods = self.db.cursor.fetchall()
            return methods  
        except Exception as e:
            print(f"Error retrieving shipment methods: {e}")

    
    
    #updating shipment method
    def update_shipment_method(self, method_id, new_method_name=None, new_region=None):
        try:
            updates = []
            params = []
        
            if new_method_name:
                updates.append("method_name = %s")
                params.append(new_method_name)
        
            if new_region:
                updates.append("region = %s")
                params.append(new_region)
        
            params.append(method_id)
        
            if updates:
                query = f"UPDATE tracker.ShipmentMethods SET {', '.join(updates)} WHERE id = %s;"
                self.db.cursor.execute(query, params)
                self.db.connection.commit()
                print(f"Shipment method {method_id} updated successfully!")
            else:
                print("No changes to update.")
    
        except Exception as e:
            print(f"Error updating shipment method: {e}")

    #getting shipment method for desired region
    def get_methods_for_region(self, region):
        try:
            query = "SELECT id, method_name FROM tracker.ShipmentMethods WHERE region = %s;"
            self.db.cursor.execute(query, (region,))
            methods = self.db.cursor.fetchall()
            if methods:
                print(f"Available shipment methods for {region}:")
                for method in methods:
                    print(f"ID: {method[0]}, Method: {method[1]}")
            else:
                print(f"No shipment methods available for region {region}")
        except Exception as e:
            print(f"Error retrieving shipment methods: {e}")

    
    
    #shipment report
    def shipment_report(self):
        query = "SELECT * FROM tracker.Order WHERE order_date IS NOT NULL AND arrival IS NULL;"
        self.db.cursor.execute(query)
        row = self.db.cursor.fetchall()
        print("Shipment Report:")
        for r in row:
            print(f"ID: {row[0]}, Boxes: {row[1]}, Date Ordered: {row[2]}, Estimated Arrival: {row[3]}, Arrival: {row[4]}, Full/Partial: {'Full' if row[5] else 'Partial'}")






    #clearing table
    def clear_table(self, table):
        self.db.clear_table(table)
        
    def close(self):
        self.db.close()
    

    
    