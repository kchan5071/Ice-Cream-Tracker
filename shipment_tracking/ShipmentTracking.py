from python_interface.database_connector import DatabaseWrapper

#shipment structure
class Shipments:
    def __init__(self, id, num_boxes, shipment_date, expected_delivery_date, actual_delivery_date, full_or_partial):
        self.id = id
        self.num_boxes = num_boxes
        self.shipment_date = shipment_date
        self.expected_delivery_date = expected_delivery_date
        self.actual_delivery_date = actual_delivery_date
        self.full_or_partial = full_or_partial
        

#operations to do on shipments
class ShipmentSystem:
    def __init__(self, user, password, host, port, database, schema):
        self.db = DatabaseWrapper(user, password, host, port, database, schema)
        self.db.connect()
    
    #insert shipment into database
    def insert_shipment(self, shipment):
        data = f"{shipment.full_or_partial}, '{shipment.actual_delivery_date}', '{shipment.expected_delivery_date}', '{shipment.shipment_date}', {shipment.num_boxes}, {shipment.id}"
        self.db.insert_data('shipments', data)
    
    #fetch all shipments from database
    def fetch_shipments(self):
        return self.db.fetch_all('shipments')
    
    def get_shipment_info(self, id):
        row = self.db.fetch_row('shipments', 'id', id)
        if row:
            row = row[0]
            num_boxes, shipment_date, expected_delivery_date, actual_delivery_date, full_or_partial = row[1], row[2].strftime('%Y-%m-%d'), row[3].strftime('%Y-%m-%d'), row[4].strftime('%Y-%m-%d'), row[5]
            return {
                'Order ID': id,
                'Date Shipped': shipment_date,
                'Shipment Boxes': num_boxes,
                'Full/Partial Shipment': 'Full' if full_or_partial else 'Partial',
                'Expected Delivery Date': expected_delivery_date,
                'Actual Delivery Date': actual_delivery_date,
            }
        else:
            return None
    
    #delete shipments by id
    def delete_shipment(self, id):
        self.db.delete_row('shipments', 'id', id)
    
    #clearing table
    def clear_table(self, table):
        self.db.clear_table(table)
        
    def close(self):
        self.db.close()
    

    
    