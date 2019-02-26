from flask import Flask, request, jsonify, Response
from pytz import timezone
from datetime import datetime
import json

from mongoslowcooker import MongoSlowcookerServer

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello from AWS-Table6-SlowCooker!"


@app.route("/rpi_address", methods=['GET', 'POST'])
def rpi_address():
    server = MongoSlowcookerServer()

    if request.method == 'GET':
        # Get the most recent RPi address entry.
        data = server.get_most_recent_from_collection('rpi_address', 1)

        if data is None:
            address = "0.0.0.0"
            date = "N/A"
        else:
            address = data[0]['address']
            date = make_pretty_date(data[0]['date'])

        return '''<h1>Address: {}</h1>
        <h1>Date: {}'''.format(address, date)

    elif request.method == 'POST':
        data = request.get_json()

        if server.verify_data(data, 'rpi_address') is True:
            data['date'] = datetime.utcnow()
            server.add_data_to_collection(data, 'rpi_address')

            address = data['address']

            return '''<h1>You said the rpi address is: {}</h1>'''.format(
                address)

        return Response(status=400)


@app.route("/temperature", methods=['GET', 'POST'])
def temperature():
    server = MongoSlowcookerServer()

    if request.method == 'GET':
        # Get the most recent RPi address entry.
        data = server.get_most_recent_from_collection('temperature', 1)

        if data is None:
            temp_type = "N/A"
            temperature = "N/A"
            measurement = "N/A"
            date = "N/A"
        else:
            temp_type = data[0]['type']
            temperature = data[0]['temperature']
            measurement = data[0]['measurement']
            date = data[0]['date']

        return jsonify(type=temp_type, temperature=temperature,
                       measurement=measurement, date=date)

    elif request.method == 'POST':
        data = request.get_json()

        if server.verify_data(data, 'temperature') is True:
            data['date'] = datetime.utcnow()
            server.add_data_to_collection(data, 'temperature')

            temperature = data['temperature']

            return '''<h1>You said the temperature is: {}</h1>'''.format(
                temperature)

        return Response(status=400)


@app.route("/cook_time", methods=['GET', 'POST'])
def cook_time():
    server = MongoSlowcookerServer()

    if request.method == 'GET':
        # Get the most recent RPi address entry.
        data = server.get_most_recent_from_collection('cook_time', 1)

        if data is None:
            start_date = "N/A"
        else:
            start_date = data[0]['start_date']

        return jsonify(start_date=start_date)

    elif request.method == 'POST':
        data = request.get_json()

        if server.verify_data(data, 'cook_time') is True:
            data['date'] = datetime.utcnow()
            server.add_data_to_collection(data, 'cook_time')

            start_date = make_pretty_date(data['start_date'])

            return '''<h1>You said the start time is: {}</h1>'''.format(
                start_date)

        return Response(status=400)


def make_pretty_date(date):
    eastern = timezone('US/Eastern')
    return '{0:%Y-%m-%d %H:%M:%S}'.format(date.astimezone(eastern))
