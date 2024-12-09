from flask import Flask, render_template, url_for, redirect, request, flash, session, abort #importing flask functions
from python_interface.database_connector import DatabaseWrapper # the database wrapper to call
from inventory_management.InventoryManagement import InventoryManagement # Inventory Management functions
from order_entry.OrderEntry import place_order # Order Entry functions
from shipment_tracking.ShipmentTracking import ShipmentSystem # Shipment Tracking functions
from trouble_ticket.functions import * # imports necessary trouble ticket functionality
from datetime import datetime
from iceapphelpers import *
import os

app = Flask(__name__)

### global variables that control site-wide functions ###

# We connect to the database as an admin and controls are distinguished here in FLask
user = 'admin'
password = 'password'
host = 'localhost'
port = '5432'
database = 'icecreamtracker'
schema = 'tracker'

db_conn = DatabaseWrapper(user, password, host, port, database, schema) # the main database wrapper where connections to the database are made
db_conn.connect() # connects us to the database
inventoryMGMT = InventoryManagement(db_conn) # controls the inventory   
shipmentMGMT = ShipmentSystem(user, password, host, port, database, schema) # controls the shipment system

    
### app routing, site page to site page ###

# starting call
@app.route('/')
def start():
    if not session.get('logged_in'):
        return render_template('icetracklogin.html')
    else:
        return home() # takes you straight to icetrackhome route
    
# the login page
@app.route('/icetracklogin.html',methods=['POST','GET'])
def login():
    session['logged_in'] = False
    return render_template('icetracklogin.html')

# when the login button is pressed
@app.route('/login',methods=['POST'])
def do_admin_login():
    global user_username
    user_username = request.form['username']
    global user_password
    user_password = request.form['password']
    global adminPriv
    # checks to see if the user exists
    if check_for_user(db_conn, 'Employee','name', user_username,'password', user_password) != []:
        session['logged_in'] = True
        # if the user exists: checks if the user has admin privileges or not
        if check_for_user_admin(db_conn, 'Employee','name', user_username,'password', user_password) != []:
            adminPriv = True
        else:
            adminPriv = False
    else:
        session['logged_in'] = False
        flash('wrong password!')
    return start()

# the signu up page
@app.route('/icetracksignup.html',methods=['POST','GET'])
def signup():
    session['logged_in'] = False
    return render_template('icetracksignup.html', message=None)

# when the sign up button is pressed
@app.route('/signup',methods=['POST','GET'])
def signupPost():
    user_username = request.form['username']
    user_password = request.form['password']
    if check_for_username(db_conn, 'Employee','name', user_username) != []:
        return render_template('icetracksignup.html',message="This user already exists")
    else:
        if user_username is not None and user_password is not None:
            print("db was called")
            result = add_employee(db_conn, 'Employee', user_username, user_password)
            print(result) # for debugging purposes
            return start()
        else:
            return render_template('icetracksignup.html',message="Fill both fields, then attempt sign up again")

# ice track home page
@app.route('/icetrackhome.html')
def home():
    return render_template('icetrackhome.html', user=user_username)

# ice track FAQ page
@app.route('/icetrackFAQ.html')
def FAQ():
    return render_template('icetrackFAQ.html', user=user_username)

# ice track order page
@app.route('/icetrackorder.html')
def order():
    return render_template('icetrackorder.html',  user=user_username)

# when the submit order button is pressd
@app.route('/icetrackordersubmitted', methods=['POST', 'GET'])
def submittedorder():
    if request.method == 'POST':
        # extracts form data
        name = str(request.form.get('customerName', '').strip())
        shippingAddress = str(request.form.get('shippingAddress', ''))
        billingAddress = str(request.form.get('billingAddress', ''))
        flavor = request.form.get('flavor','')
        size = request.form.get('size','')
        quantity = int(request.form.get('quantity',''))

        # price calculations
        sizePrice = 1
        price = 0

        if size == 'S':
            sizePrice = 2.99
        elif size == 'M':
            sizePrice = 3.99
        elif size == 'L':
            sizePrice = 4.992

        price = sizePrice * quantity 

        try:
            # places the order
            success = place_order(db_conn, name, shippingAddress, billingAddress, [(flavor,size,quantity,price)], "Standard", "ok")
            return render_template('icetrackordersubmitted.html',status=success, user=user_username)

        except Exception as e:
            print(f"Error placing order: {e}")  # logs the error
            return render_template('icetrackordersubmitted.html', status="error", error_message=str(e),  user=user_username)

    return render_template('icetrackordersubmitted.html', status="invalid", user=user_username)

# ice track inventory page
@app.route('/icetrackinventory.html',methods=['POST','GET'])
def inventory():
    results = inventoryMGMT.get_inventory_status()
    return render_template('icetrackinventory.html',inventory=results, user=user_username, adminPriv=adminPriv)

# when the commit button is pressed (only accessible by admin)
@app.route('/commitInv',methods=['POST','GET'])
def commitInv():
    givenID = int(request.form.get('commitNum',0))
    inventoryMGMT.update_commited(givenID)
    return inventory()

# when the add button is pressed (only accessible by admin)
@app.route('/addInv',methods=['POST','GET'])
def addInv():
    givenID = int(request.form.get('addNum',0))
    inventoryMGMT.increment_available(givenID)
    return inventory()


# when the defective button is pressed (only accessible by admin)
@app.route('/defectiveInv',methods=['POST','GET'])
def defectiveInv():
    givenID = int(request.form.get('defectiveNum',0))
    inventoryMGMT.update_defective(givenID)
    return inventory()


# when the delete button is pressed (only accessible by admin)
@app.route('/deleteInv',methods=['POST','GET'])
def deleteInv():
    givenID = int(request.form.get('deleteNum',0))
    inventoryMGMT.decrement_available(givenID)
    return inventory()


# when the add new ice cream button is pressed (only accessible by admin)
@app.route('/icetracknewinventory',methods=['POST','GET'])
def newInv():
    givenID = int(request.form.get('id',0))
    flavor = request.form.get('flavor','')
    size = request.form.get('size','')
    # cost calculations (matching the order submission)
    if size == 'S':
        sizePrice = 2.99
    elif size == 'M':
        sizePrice = 3.99
    elif size == 'L':
        sizePrice = 4.99
    cost = sizePrice
    available = int(request.form.get('quantity',0))
    committed = 0
    defective = 0
    # adding product based on gathered info
    inventoryMGMT.add_product(givenID, flavor, size, cost, available, committed, defective)
    return inventory()

# ice track shipment page
@app.route('/icetrackshipment.html',methods=['GET'])
def shipment():
    return render_template('icetrackshipment.html', user=user_username)

# when the track shipment button is pressed
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
            orderDate = datetime.strptime(orderDate,'%Y-%m-%d') if orderDate else None
            estimatedArrival = datetime.strptime(estimatedArrival,'%Y-%m-%d') if estimatedArrival else None

            # Validate inputs
            if not name:
                app.logger.error("Company name is missing.")
                return render_template('icetrackshipment.html', foundStatus=None, error="Company name is required.", user=user_username)

            # Query shipment status
            if shipmentMGMT:
                shipmentStatus = shipmentMGMT.query_shipments(name, orderDate, estimatedArrival)

                if shipmentStatus and len(shipmentStatus) > 0:
                    # Fetch detailed shipment information
                    shipments = []
                    for shipment in shipmentStatus:
                        shipments.append(shipmentMGMT.get_shipment_info(shipment[0]))
                
                    for show in shipments:
                        print(show)
                    return render_template('icetrackshipment.html', foundStatus=shipments)
                else:
                    app.logger.info("No shipment found for given criteria.")
                    return render_template('icetrackshipment.html', foundStatus=None, error="No shipments match your search criteria.", user=user_username)
            else:
                app.logger.error("shipmentMGMT is not initialized.")
                return render_template('icetrackshipment.html', foundStatus=None, error="Shipment management system unavailable.", user=user_username)

        # Handle GET request or return empty form
        return render_template('icetrackshipment.html', foundStatus=None)

    except ValueError as ve:
        app.logger.error("ValueError encountered: %s", ve)
        return render_template('icetrackshipment.html', foundStatus=None, error="Invalid data provided. Please check your inputs.", user=user_username)

    except Exception as e:
        app.logger.exception("Unexpected error in trackShipment: %s", e)
        return render_template('icetrackshipment.html', foundStatus=None, error="An unexpected error occurred. Please try again.", user=user_username)

# ice track trouble ticket page
@app.route('/icetrackticketmgmt.html')
def ticketentry():
    tickets = view_open_tickets(db_conn)
    for ticket in tickets:
        print(ticket)
    return render_template('icetrackticketmgmt.html', open_tickets=tickets, user=user_username, adminPriv=adminPriv)

# when the close ticket button is pressed (only accessible by admin)
@app.route('/resolveTicket',methods=['POST','GET'])
def resolveTicket():
    try:
        if request.method == 'POST':
            # Debugging: Log form data
            app.logger.info("Form data: %s", request.form)

            # Extract and format form data
            ticketID = int(request.form.get('ticketID', ''))
            resolution = request.form.get('resolution', '')

            
            # Find and update ticket status
            update_ticket_status(db_conn, ticketID, 'closed', resolution)
        # Handle GET request or return empty form
        return ticketentry()

    except ValueError as ve:
        app.logger.error("ValueError encountered: %s", ve)
        return ticketentry()
    except Exception as e:
        app.logger.exception("Unexpected error in trackShipment: %s", e)
        return ticketentry()

# when an trouble ticket is made and the submit button is pressed
@app.route('/icetrackticketsubmitted', methods=['POST', 'GET'])
def ticketsubmitted():
    if request.method == 'POST':

        # Extract and format form data
        name = request.form.get('sourceName', '').strip()  # Safeguard against missing keys
        date_detected = request.form.get('detectionDate', '')
        problem_type = request.form.get('problemType','')
        description = request.form.get('problemDescription', '')

        try:
            success = create_ticket(db_conn, name, date_detected, problem_type, description, status = 'open', resolution=None)    
            return render_template('icetrackticketsubmitted.html', state = success, user=user_username)
            
        except Exception as e:
            print(f"Error placing order: {e}")  # Log the error for debugging
            return render_template('icetrackticketsubmitted.html', state="error", error_message=str(e), user=user_username)

    return render_template('icetrackticketsubmitted.html', state = "invalid", user=user_username)
    
# app name
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)