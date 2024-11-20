from flask import Flask, render_template, url_for, redirect, request


app = Flask(__name__)

# app routing, site page to site page
@app.route('/')
def start():
    return home()

@app.route('/icetrackhome.html')
def home():
    return render_template('icetrackhome.html')

@app.route('/icetrackFAQ.html')
def FAQ():
    return render_template('icetrackFAQ.html')

@app.route('/icetrackorder.html')
def order():
    return render_template('icetrackorder.html')

@app.route('/icetrackordersubmitted',methods=['POST','GET'])
def submittedorder():
    if request.method=='POST':
        name=str(request.form['name'])
        shippingAddress=str(request.form['shippingAddress'])
        billingAddress=str(request.form['billingAddress'])
        orderDescription=str(request.form['orderDescription'])
        subtotal=float(request.form['subtotal'])
        shippingCost=float(request.form['shippingCost'])
        totalCost=float(request.form['totalCost'])
        orderDate=request.form['orderDate']
        paymentDate=request.form['paymentDate']
        customerStatus=str(request.form['customerStatus'])
        submitted="icetrackordersubmitted.html"
    #return redirect(url_for(submitted))
    # if info can get passed to db, then show success, else show fail
    return render_template('icetrackordersubmitted.html')

@app.route('/icetrackordersubmitted.html')
def ordersubmitted():
    return render_template('icetrackordersubmitted.html')

@app.route('/icetrackinventory.html',methods=['POST','GET'])
def inventory():
    return render_template('icetrackinventory.html')

@app.route('/icetrackshipment.html',methods=['POST','GET'])
def shipment():
    return render_template('icetrackshipment.html')

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
