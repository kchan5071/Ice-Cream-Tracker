import sys
import os

# Add the parent directory (Ice-Cream-Tracker) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shipment_tracking.ShipmentTracking import ShipmentSystem


def main():   
    # Create the shipment system
    db = ShipmentSystem(user='admin', password='password', host='localhost', port='5432', database='icecreamtracker', schema='tracker')
    
    #example for id 1
    db.add_shipment_info(1, 'Company 1', 10, '2024-10-03', '2025-10-28', '2021-10-01', True, None)
    print(db.get_shipment_info(1))

    #undelivered shipment example
    db.add_shipment_info(2, 'Company 2', 5, '2024-10-03', '2025-10-28', None , True, None)
    print(db.get_shipment_info(2))
    
    #undelivered shipment example, then update status
    db.add_shipment_info(3, 'Company 3', 5, '2024-10-03', '2025-10-28', None , True, None)
    print(db.get_shipment_info(2))
    
    #testing update status
    db.update_shipment_info(3, '2024-11-11')
    print(db.get_shipment_info(3))
    
    #shipment status report
    print(db.shipment_report())
    
    
    
    #user-admin list for shipment options
    db.add_shipment_method('Standard Shipping', 'North America')
    db.add_shipment_method('Express Shipping', 'North America')
    db.add_shipment_method('International Shipping', 'International')

    #showing all shipment methods
    db.get_methods_for_region('North America')
    db.get_methods_for_region('International')
    
    #testing updating shipping method by order id
    db.update_shipment_method(1, 2)
    db.get_shipment_method_info(1)
    
    
    
    
    #clear table for next run
    db.clear_table('order')
    db.clear_table('ShipmentMethods')
    
    # Close the connection
    db.close()
    
if __name__ == '__main__':
    main()
