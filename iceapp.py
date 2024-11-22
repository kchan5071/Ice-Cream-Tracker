from flask import Flask, render_template, url_for, redirect, request #importing flask functions
from python_interface.database_connector import DatabaseWrapper # the database wrapper to call
from inventory_management.InventoryManagement import InventoryManagement # Inventory Management functions
from order_entry.OrderEntry import place_order # Order Entry functions
from shipment_tracking.ShipmentTracking import ShipmentSystem # Shipment Tracking functions

app = Flask(__name__)

def startup():
    user = 'admin'
    password = 'password'
    host = 'localhost'
    port = '5432'
    database = 'icecreamtracker'
    schema = 'tracker'
    global db_conn
    db_conn = DatabaseWrapper(user, password, host, port, database, schema)
    db_conn.connect()
    global inventoryMGMT
    inventoryMGMT = InventoryManagement(db_conn)
    global shipmentMGMT
    shipmentMGMT = ShipmentSystem(user, password, host, port, database, schema)
# app routing, site page to site page

# starting call
@app.route('/')
def start():
    startup()
    return home() # takes you straight to icetrackhome route

@app.route('/icetrackhome.html')
def home():
    return render_template('icetrackhome.html')

@app.route('/icetrackFAQ.html')
def FAQ():
    return render_template('icetrackFAQ.html')

@app.route('/icetrackorder.html')
def order():
    return render_template('icetrackorder.html')

@app.route('/icetrackordersubmitted', methods=['POST', 'GET'])
def submittedorder():
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name', '').strip()
        shippingAddress = request.form.get('shippingAddress', '')
        billingAddress = request.form.get('billingAddress', '')
        orderDescription = request.form.get('orderDescription', '')
        customerStatus = request.form.get('customerStatus', '').strip()

        try:
            # Place the order
            success = place_order(db_conn, name, shippingAddress, billingAddress, orderDescription, "standard", customerStatus)

            # Render success or failure template based on result
            if success:
                return render_template('icetrackordersubmitted.html', status="success")
            else:
                return render_template('icetrackordersubmitted.html', status="failure")

        except Exception as e:
            print(f"Error placing order: {e}")  # Log the error for debugging
            return render_template('icetrackordersubmitted.html', status="error", error_message=str(e))

    # Handle GET request (optional)
    return render_template('icetrackordersubmitted.html', status="invalid")

@app.route('/icetrackordersubmitted.html', methods=['POST', 'GET'])
def ordersubmitted():
    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name', '').strip()
        shippingAddress = request.form.get('shippingAddress', '')
        billingAddress = request.form.get('billingAddress', '')
        orderDescription = request.form.get('orderDescription', '')
        customerStatus = request.form.get('customerStatus', '').strip()

        try:
            # Place the order
            success = place_order(db_conn, name, shippingAddress, billingAddress, orderDescription, "standard", customerStatus)

            # Render success or failure template based on result
            if success:
                return render_template('icetrackordersubmitted.html', status="success")
            else:
                return render_template('icetrackordersubmitted.html', status="failure")

        except Exception as e:
            print(f"Error placing order: {e}")  # Log the error for debugging
            return render_template('icetrackordersubmitted.html', status="error", error_message=str(e))

    # Handle GET request (optional)
    return render_template('icetrackordersubmitted.html', status="invalid")


@app.route('/icetrackinventory.html',methods=['POST','GET'])
def inventory():
    results = inventoryMGMT.get_inventory_status()
    return render_template('icetrackinventory.html',inventory=results)

@app.route('/commitInv',methods=['POST','GET'])
def commitInv():
    givenID = int(request.form.get('commitNum',0))
    inventoryMGMT.update_commited(givenID)
    return inventory()

@app.route('/addInv',methods=['POST','GET'])
def addInv():
    givenID = int(request.form.get('addNum',0))
    inventoryMGMT.increment_available(givenID)
    return inventory()

@app.route('/defectiveInv',methods=['POST','GET'])
def defectiveInv():
    givenID = int(request.form.get('defectiveNum',0))
    inventoryMGMT.update_defective(givenID)
    return inventory()

@app.route('/deleteInv',methods=['POST','GET'])
def deleteInv():
    givenID = int(request.form.get('deleteNum',0))
    inventoryMGMT.decrement_available(givenID)
    return inventory()

@app.route('/icetrackshipment.html',methods=['GET'])
def shipment():
    # shipmentStatus = shipmentMGMT.query_shipments(None,None,None)
    return render_template('icetrackshipment.html')

@app.route('/trackShipment', methods=['POST', 'GET'])
def trackShipment():
    if request.method == 'POST':
        # Debugging: Print form data
        print(request.form)

        # Extract and format form data
        name = request.form.get('companyName', '').strip()  # Safeguard against missing keys
        orderDate = request.form.get('orderDate', '')       # Optional fallback: empty string
        estimatedArrival = request.form.get('estimatedArrival', '')

        # Handle formatting dates (ensure format_date is robust and tested)
        orderDate = format_date(orderDate) if orderDate else None
        estimatedArrival = format_date(estimatedArrival) if estimatedArrival else None

        # Query shipment status
        shipmentStatus = shipmentMGMT.query_shipments(name, orderDate, estimatedArrival)

        # Debugging: Print the result
        print(shipmentStatus)

        # Return results to the template
        return render_template('icetrackshipment.html', foundStatus=shipmentStatus)
    
    # Handle GET request or return empty form
    return render_template('icetrackshipment.html', foundStatus=None)


@app.route('/icetrackticketmgmt.html')
def ticketentry():
    return render_template('icetrackticketmgmt.html')

@app.route('/icetrackticketsubmitted.html')
def ticketsubmitted():
    return render_template('icetrackticketsubmitted.html')

@app.route('/icetracklogin.html',methods=['POST','GET'])
def login():
    return render_template('icetracklogin.html')

@app.route('/icetracksignup.html',methods=['POST','GET'])
def signup():
    return render_template('icetracksignup.html')


if __name__ == '__main__':
    app.run(debug=True)
