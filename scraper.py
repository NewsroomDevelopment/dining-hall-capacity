from utils import *
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import requests

# get capacity percentages
def get_capacity(crowd_size, max_size):
    return str(round(int(crowd_size)/int(max_size), 2))


# Load environment variables
load_dotenv(os.getenv('MDB_PASSWORD'))

# Connect to MongoDB
MDB_USERNAME = os.getenv('MDB_USERNAME')
MDB_PASSWORD = os.getenv('MDB_PASSWORD')
MDB_URI = f'mongodb+srv://{MDB_USERNAME}:{MDB_PASSWORD}@capacitydata.tmbif.mongodb.net/capacityData?retryWrites=true&w=majority'

client = MongoClient(MDB_URI)

# Get JSON Files
crowdedness_site = "https://dining.columbia.edu/cu_dining/rest/crowdedness"

crowd_data_r = requests.get(crowdedness_site)

crowd_data = []

if crowd_data_r.status_code == 403:
    print("failed fetch. Please retry.")
else:
    crowd_data = crowd_data_r.json()['data']

# Dining Parameters
dining_halls = {
    155: {
        'name': 'John Jay Dining Hall',
        'max_size': 246
    },
    192: {
        'name': 'JJ\'s place',
        'max_size': 104
    },
    104: {
        'name': 'Ferris Booth Commons',
        'max_size': 264
    }
}

data_obj = {
    '_id': str(pd.Timestamp.today())
}
# Get Data
for key, info in dining_halls.items():
    client_count = crowd_data[str(key)]['client_count']
    max_size = info['max_size']
    data_obj[info['name']] = {
        'client_count': client_count,
        'capacity': get_capacity(client_count, max_size)
    }


db = client["dining_hall_data"]
collection = db['data']
collection.insert_one(data_obj)
