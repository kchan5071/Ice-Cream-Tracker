from flask import Flask, render_template, url_for, redirect, request #importing flask functions
from python_interface.database_connector import DatabaseWrapper # the database wrapper to call
from inventory_management.InventoryManagement import InventoryManagement # Inventory Management functions
from order_entry.OrderEntry import place_order # Order Entry functions
from shipment_tracking.ShipmentTracking import ShipmentSystem # Shipment Tracking functions
from trouble_ticket.functions import create_ticket # imports necessary trouble ticket functionality
from datetime import datetime


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
    return render_template('icetrackshipment.html')

@app.route('/trackShipment', methods=['POST', 'GET'])
def trackShipment():
    try:
        if request.method == 'POST':
            # Debugging: Log form data
            app.logger.info("Form data: %s", request.form)

            # Extract and format form data
            name = request.form.get('companyName', '').strip()
            orderDate = request.form.get('orderDate', '')
            estimatedArrival = request.form.get('estimatedArrival', '')

            # Handle date formatting with validation
            orderDate = format_date(orderDate) if orderDate else None
            estimatedArrival = format_date(estimatedArrival) if estimatedArrival else None

            # Validate inputs
            if not name:
                app.logger.error("Company name is missing.")
                return render_template('icetrackshipment.html', foundStatus=None, error="Company name is required.")

            # Query shipment status
            if shipmentMGMT:
                shipmentStatus = shipmentMGMT.query_shipments(name, orderDate, estimatedArrival)

                if shipmentStatus and len(shipmentStatus) > 0:
                    # Fetch detailed shipment information
                    shipmentShow = shipmentMGMT.get_shipment_info(shipmentStatus[0][0])
                    return render_template('icetrackshipment.html', foundStatus=shipmentShow)
                else:
                    app.logger.info("No shipment found for given criteria.")
                    return render_template('icetrackshipment.html', foundStatus=None, error="No shipments match your search criteria.")
            else:
                app.logger.error("shipmentMGMT is not initialized.")
                return render_template('icetrackshipment.html', foundStatus=None, error="Shipment management system unavailable.")

        # Handle GET request or return empty form
        return render_template('icetrackshipment.html', foundStatus=None)

    except ValueError as ve:
        app.logger.error("ValueError encountered: %s", ve)
        return render_template('icetrackshipment.html', foundStatus=None, error="Invalid data provided. Please check your inputs.")

    except Exception as e:
        app.logger.exception("Unexpected error in trackShipment: %s", e)
        return render_template('icetrackshipment.html', foundStatus=None, error="An unexpected error occurred. Please try again.")


@app.route('/icetrackticketmgmt.html', methods=['POST', 'GET'])
def ticketentry():
    return render_template('icetrackticketmgmt.html')

@app.route('/icetrackticketsubmitted.html', methods=['POST', 'GET'])
def submittedticket():
    return render_template('icetrackticketsubmitted.html')

@app.route('/icetrackticketsubmitted', methods=['POST', 'GET'])
def ticketsubmitted():
    if request.method == 'POST':

        # Extract and format form data
        name = request.form.get('name', '').strip()  # Safeguard against missing keys
        date_detected = request.form.get('dateDetected', '')
        problem_type = request.form.get('problemType','')
        description = request.form.get('problemDescription', '')

        date_detected = format_date(date_detected) if date_detected else None

        try:
            # create the ticket
            success = create_ticket(db_conn, None, name, date_detected, problem_type, description, status = 'open', resolution=None)

            # Render success or failure template based on result
            if success:
                return render_template('icetrackticketsubmitted.html', status="success")
            else:
                return render_template('icetrackticketsubmitted.html', status="failure")

        except Exception as e:
            print(f"Error placing order: {e}")  # Log the error for debugging
            return render_template('icetrackticketsubmitted.html', status="error", error_message=str(e))

    return render_template('icetrackticketsubmitted.html', status = "invalid")
    

@app.route('/icetracklogin.html',methods=['POST','GET'])
def login():
    return render_template('icetracklogin.html')

@app.route('/icetracksignup.html',methods=['POST','GET'])
def signup():
    return render_template('icetracksignup.html')


if __name__ == '__main__':
    app.run(debug=True)



# helpers
def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()  # Adjust format as needed
    except ValueError:
        print("Invalid date format:", date_str)
        return None
