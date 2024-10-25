import sys
import os

# Add the parent directory (Ice-Cream-Tracker) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shipment_tracking.ShipmentTracking import Shipments, ShipmentSystem
from shipment_tracking.admin_interface import admin_interface

def main():   
    # Create the shipment system
    db = ShipmentSystem(user='admin', password='password', host='localhost', port='5432', database='icecreamtracker', schema='tracker')
    
    #example for id 1
    db.add_shipment_info(1, 2, '2021-10-15', '2024-01-10', '2024-11-11', True, 'McDonalds')
    print(db.get_shipment_info(1))

    #undelivered shipment example
    db.add_shipment_info(2, 2, '2024-10-15', '2024-01-10', None, True, 'McDonalds')
    print(db.get_shipment_info(2))
    
    #testing update status
    db.update_shipment_info(2, '2024-11-11')
    print(db.get_shipment_info(2))
    
    #db.get_methods_for_region('North America')
    
   # db.update_shipment_method(1, 'UPS', 'North America')
    #print(db.get_shipment_info(1))
    
    #clear table for next run
    db.clear_table('Order')
    
    # Close the connection
    db.close()
    
if __name__ == '__main__':
    main()
