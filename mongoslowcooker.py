#!/usr/bin/env python3

from pymongo import MongoClient, DESCENDING
from pytz import timezone
from datetime import datetime
import json
import requests
import threading


collection_requirements = {'rpi_address': ['address'],
                           'temperature': ['type',
                                           'temperature',
                                           'measurement'],
                           'cook_time': ['start_time'],
                           'lid_status': ['status']}


class MongoSlowcookerServer:
    '''A wrapper for the pymongo MongoClient class.'''

    def __init__(self):
        self.database_name = "slow_cooker"
        self.client = MongoClient()
        self.db = self.client[self.database_name]

    # Gets the collection if the given name is in the dict of collections.
    # Returns the collection object or None on failure.
    def get_collection_by_name(self, name):
        if name not in collection_requirements:
            return None

        return self.db[name]

    # Adds the given data to the given collection. Return the document id on
    # success, None on failure.
    def add_data_to_collection(self, data, name):
        if name not in collection_requirements:
            return None

        if self.verify_data(data, name) is False:
            return None

        collection = self.db[name]
        data['date'] = datetime.utcnow()
        return collection.insert_one(data).inserted_id

    # Checks if the data meets the requirements of the collection. True if
    # success, false if the given collection name is not in the database or
    # the data does not meet the requirements of the collection.
    def verify_data(self, data, collection):
        if collection not in collection_requirements:
            return False

        requirements = collection_requirements[collection]

        if len(data) != len(requirements):
            return False

        for k in data.keys():
            if k not in requirements:
                return False

        return True

    # Get's the n most recent documents from the given collection or empty
    # list if either the collection doesn't exist or if the collection is
    # empty. Note that the given n might be larger than the size of the
    # given collection.
    def get_most_recent_from_collection(self, name, n):
        data = []
        if name in collection_requirements:
            collection = self.db[name]
            for doc in collection.find().sort([('date', DESCENDING)]).limit(n):
                data.append(doc)

        return data


class MongoSlowcookerClient:
    '''An abstraction around the requests and json modules suited for
    JSON POST requests.'''

    def __init__(self, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port

    # Pushes the given data to the server directory specified by the given
    # destination. Do not call this function directly; call
    # add_data_to_collection instead.
    def push_to_server(self, data, destination):
        http = "http://{}:{}/{}".format(self.ip_addr, self.port, destination)
        header = {'Content-Type': 'application/json'}
        requests.post(http, data=json.dumps(data), headers=header)

    # Adds the given data to the given collection if the data is valid. Return
    # None on failure.
    def add_data_to_collection(self, data, destination):
        if destination not in collection_requirements:
            print('MongoSlowcookerClient: Name "{}" not a supported web page.'
                  'Check spelling.'.format(destination))
            return None

        if self.verify_data(data, destination) is False:
            return None

        # It would be useful if we could get the return result from the thread.
        # Some brief research shows that using a ThreadPool might be useful for
        # that but did not have much success in practice.
        threading.Thread(target=self.push_to_server,
                         args=(data, destination)).start()

    # Checks if the data meets the requirements of the collection. True
    # if success, false if the given collection name is not in the
    # database or the data does not meet the requirements of the
    # collection.
    def verify_data(self, data, collection):
        if collection not in collection_requirements:
            print('MongoSlowcookerClient: Name "{}" not a supported '
                  'collection. Check spelling.'.format(collection))
            return False

        requirements = collection_requirements[collection]

        if len(data) != len(requirements):
            print('MongoSlowcookerClient: Length of data incorrect. Check '
                  'collection spec sheet.')
            return False

        for k in data.keys():
            if k not in requirements:
                print('MongoSlowcookerClient: Key "{}" not supported in '
                      'collection "{}".'.format(k, collection))
                return False

        return True
