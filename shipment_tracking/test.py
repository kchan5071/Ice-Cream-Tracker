from shipment_tracking.ShipmentTracking import Shipments, ShipmentSystem
    
# Create the shipment system
shipment_system = ShipmentSystem(user='brenda', password='password', host='localhost', port='5432', database='icecreamtracker', schema='tracker')

# Add a shipment
shipment1 = Shipments(full_or_partial=True, actual_delivery_date='2024-11-11', expected_delivery_date='2024-01-10', shipment_date='2024-10-15', num_boxes=2, id=1)
shipment_system.insert_shipment(shipment1)

shipment2 = Shipments(full_or_partial=True, actual_delivery_date='2024-12-12', expected_delivery_date='2024-02-10', shipment_date='2024-10-15', num_boxes=5, id=2)
shipment_system.insert_shipment(shipment2)


# Delete a shipment
shipment_system.delete_shipment(1)
    
shipment3 = Shipments(full_or_partial=True, actual_delivery_date='2024-12-12', expected_delivery_date='2024-03-10', shipment_date='2024-10-15', num_boxes=6, id=3)
shipment_system.insert_shipment(shipment3)

info = shipment_system.get_shipment_info(3)
print(info)

# Fetch all shipments
shipments = shipment_system.fetch_shipments()
for shipment in shipments:
    print(shipment)

#clearing for next run
shipment_system.clear_table('shipments')

# Close the connection
shipment_system.close()
