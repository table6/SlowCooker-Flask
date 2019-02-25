from flask import Flask
from flask import request
from pymongo import MongoClient, DESCENDING
from pytz import timezone
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from AWS-Table6-SlowCooker!"

@app.route("/rpi-address", methods=['GET', 'POST'])
def rpi_address():
    # Initialize MongoDB client.
    client = MongoClient()
    db = client.slow_cooker
    collection = db.rpi_address
    
    if request.method == 'GET':
        # Get the most recent RPi address entry.
        for doc in collection.find().sort([('date', DESCENDING)]).limit(1):
            data = doc
        
        if data == None:
            address = "0.0.0.0"
            date = "N/A"
        else:
            address = data['address']
            date = make_pretty_date(data['date'])

        return '''<h1>Address: {}</h1>
        <h1>Date: {}'''.format(address, date)

    elif request.method == 'POST':
        data = request.get_json()
        address = data['address']

        # Write address to database.
        data = {"address": address, "date": datetime.utcnow()}
        collection.insert_one(data)

        return '''<h1>You said the rpi address is: {}</h1>'''.format(address)

def make_pretty_date(date):
    eastern = timezone('US/Eastern')
    return '{0:%Y-%m-%d %H:%M:%S}'.format(date.astimezone(eastern))
        
