from utils import *
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import requests

#get capacity percentages
def get_capacity(hall):
  return int(crowd_data['data'][str(hall)]['client_count'])/int(dining_halls[hall]['max_size'])

# Load environment variables
load_dotenv(os.getenv('MDB_PASSWORD'))

# Connect to MongoDB
MDB_USERNAME = os.getenv('MDB_USERNAME')
MDB_PASSWORD = os.getenv('MDB_PASSWORD')

MDB_URI = f'mongodb+srv://{MDB_USERNAME}:{MDB_PASSWORD}@capacitydata.tmbif.mongodb.net/capacityData?retryWrites=true&w=majority'

client = MongoClient(MDB_URI)

#Get JSON Files
crowdedness_site = "https://dining.columbia.edu/cu_dining/rest/crowdedness"
dining_site = "https://dining.columbia.edu/sites/default/files/cu_dining/cu_dining_nodes.json"

crowd_data_r = requests.get(crowdedness_site)
dining_data_r = requests.get(dining_site)

crowd_data = []
dining_data = []

if crowd_data_r.status_code == 403:
  print("failed fetch")
else:
  crowd_data = crowd_data_r.json()

if dining_data_r.status_code == 403:
  print("failed fetch")
else:
  dining_data = dining_data_r.json()

#Dining Parameters
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

#Get Data
for hall in dining_halls:
  capacity = dining_halls[hall]['name'] + ": " + str(get_capacity(hall))
  dining_halls[hall]['capacity'] = capacity

current_time = str(pd.Timestamp.today())

db = client["dining_hall_data"]
collection = db[current_time]
collection.insert_one(dining_halls)

