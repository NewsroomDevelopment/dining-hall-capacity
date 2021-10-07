from utils import *
import pandas as pd
import json
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
import os

# Load environment variables
load_dotenv(os.getenv('MDB_PASSWORD'))

# Connect to MongoDB
MDB_USERNAME = os.getenv('MDB_USERNAME')
MDB_PASSWORD = os.getenv('MDB_PASSWORD')

MDB_URI = f'mongodb+srv://{MDB_USERNAME}:{MDB_PASSWORD}@capacitydata.tmbif.mongodb.net/capacityData?retryWrites=true&w=majority'

client = MongoClient(MDB_URI)
