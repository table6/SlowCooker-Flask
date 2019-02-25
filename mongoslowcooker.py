from pymongo import MongoClient, DESCENDING
from pytz import timezone
from datetime import datetime
import json

class MongoSlowcookerClient:
    '''A wrapper for the pymongo MongoClient class. '''
    
    def __init__(self):
        self.database_name = "slow_cooker"
        self.collections = ['rpi_address', 'temperature', 'cook_time']

        self.client = MongoClient()
        self.db = self.client[self.database_name]


    # Gets the collection if the given name is in the dict of 
    # collections. None on failure.
    def get_collection_by_name(self, name):
        # Protect against adding unecessary collections.
        if name not in self.collections:
            return None
        
        return self.db[name]


    # Adds the given data to the given collection. Return the id on 
    # success, None on failure.
    def add_data_to_collection(self, data, name):
        if name not in self.collections:
            return None

        collection = self.db[name]

        # Should verify contents with regex. For now, check size of data.
        if name == 'rpi_address':
            # Require address.
            if len(data) != 1:
                return None

            if 'address' not in data:
                return None

            data['date'] = datetime.utcnow()
            return collection.insert_one(data)

        elif name == 'temperature':
            # Require type, temperature, and measurement.
            if len(data) != 3:
                return None

        elif name == 'cook_time':
            # Require start_date.
            if len(data) != 1:
                return None

        return None


    def get_most_recent_from_collection(self, name):
        if name not in self.collections:
            return None

        data = None
        collection = self.db[name]
        for doc in collection.find().sort([('date', DESCENDING)]).limit(1):
            data = doc

        return data
