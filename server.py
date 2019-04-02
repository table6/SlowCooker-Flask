from flask import Flask, request, jsonify, Response
from pytz import timezone
from datetime import datetime

from mongoslowcooker import MongoSlowcookerServer

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello from AWS-Table6-SlowCooker!"


@app.route("/rpi_address", methods=['GET', 'POST'])
def rpi_address():
    server = MongoSlowcookerServer()

    if request.method == 'GET':
        data = server.get_most_recent_from_collection('rpi_address', 1)

        if len(data) == 0:
            address = "N/A"
            date = "N/A"
        else:
            address = data[0]['address']
            date = make_pretty_date(data[0]['date'])

        return '''<h1>Address: {}</h1>
            <h1>Date: {}'''.format(address, date)

    elif request.method == 'POST':
        data = request.get_json()

        if server.verify_data(data, 'rpi_address') is True:
            server.add_data_to_collection(data, 'rpi_address')

            address = data['address']

            return '''<h1>You said the rpi address is: {}</h1>'''.format(
                address)

        return Response(status=400)


@app.route("/temperature", methods=['GET', 'POST'])
def temperature():
    server = MongoSlowcookerServer()

    if request.method == 'GET':
        data = server.get_most_recent_from_collection('temperature', 1)

        if len(data) == 0:
            data = {'type': 'N/A', 'temperature': 'N/A',
                    'measurement': 'N/A', 'date': 'N/A'}
        else:
            data = {'type': data[0]['type'],
                    'temperature': data[0]['temperature'],
                    'measurement': data[0]['measurement'],
                    'date': data[0]['date']}

        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()

        if server.verify_data(data, 'temperature') is True:
            server.add_data_to_collection(data, 'temperature')

            temperature = data['temperature']

            return '''<h1>You said the temperature is: {}</h1>'''.format(
                temperature)

        return Response(status=400)


@app.route("/cook_time", methods=['GET', 'POST'])
def cook_time():
    server = MongoSlowcookerServer()

    if request.method == 'GET':
        data = server.get_most_recent_from_collection('cook_time', 1)

        if len(data) == 0:
            data = {'start_time': 'N/A', 'date': 'N/A'}
        else:
            data = {'start_time': data[0]['start_time'],
                    'date': data[0]['date']}

        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()

        if server.verify_data(data, 'cook_time') is True:
            server.add_data_to_collection(data, 'cook_time')

            start_time = make_pretty_date(data['start_time'])

            return '''<h1>You said the start time is: {}</h1>'''.format(
                start_time)

        return Response(status=400)


@app.route("/lid_status", methods=['GET', 'POST'])
def lid_status():
    server = MongoSlowcookerServer()

    if request.method == 'GET':
        data = server.get_most_recent_from_collection('lid_status', 1)

        if len(data) == 0:
            data = {'status': 'N/A'}
        else:
            data = {'status': data[0]['status'],
                    'date': data[0]['date']}

        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()

        if server.verify_data(data, 'lid_status') is True:
            server.add_data_to_collection(data, 'lid_status')

            status = data['status']

            return '''<h1>You said the status is: {}</h1>'''.format(
                status)

        return Response(status=400)


@app.route("/control_temperature", methods=['GET', 'POST'])
def control_temperature():
    server = MongoSlowcookerServer()

    if request.method == 'GET':
        data = server.get_most_recent_from_collection('control_temperature', 1)

        if len(data) == 0:
            data = {'type': 'N/A', 'temperature': 'N/A',
                    'measurement': 'N/A', 'date': 'N/A'}
        else:
            data = {'type': data[0]['type'],
                    'temperature': data[0]['temperature'],
                    'measurement': data[0]['measurement'],
                    'date': data[0]['date']}

        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()

        if server.verify_data(data, 'control_temperature') is True:
            server.add_data_to_collection(data, 'control_temperature')

            temperature = data['temperature']

            return '''<h1>You said the temperature is: {}</h1>'''.format(
                temperature)

        return Response(status=400)


@app.route("/control_cook_time", methods=['GET', 'POST'])
def control_cook_time():
    server = MongoSlowcookerServer()

    if request.method == 'GET':
        data = server.get_most_recent_from_collection('control_cook_time', 1)

        if len(data) == 0:
            data = {'start_time': 'N/A', 'date': 'N/A'}
        else:
            data = {'start_time': data[0]['start_time'],
                    'date': data[0]['date']}

        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()

        if server.verify_data(data, 'control_cook_time') is True:
            server.add_data_to_collection(data, 'control_cook_time')

            start_time = data['start_time']

            return '''<h1>You said the start time is: {}</h1>'''.format(
                start_time)

        return Response(status=400)


@app.route("/control_lid_status", methods=['GET', 'POST'])
def control_lid_status():
    server = MongoSlowcookerServer()

    if request.method == 'GET':
        data = server.get_most_recent_from_collection('control_lid_status', 1)

        if len(data) == 0:
            data = {'status': 'N/A'}
        else:
            data = {'status': data[0]['status'],
                    'date': data[0]['date']}

        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()

        if server.verify_data(data, 'control_lid_status') is True:
            server.add_data_to_collection(data, 'control_lid_status')

            status = data['status']

            return '''<h1>You said the status is: {}</h1>'''.format(
                status)

        return Response(status=400)


def make_pretty_date(date):
    if type(date) is str:
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

    eastern = timezone('US/Eastern')
    return '{0:%Y-%m-%d %H:%M:%S}'.format(date.astimezone(eastern))
