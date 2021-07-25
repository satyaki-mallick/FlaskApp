

import pprint
import pymongo

from pymongo import MongoClient
mongo_client = MongoClient("mongodb+srv://db-admin-satyaki:admin@cluster0.kkrlk.mongodb.net/MyFirstDatabase?retryWrites=true&w"
                     "=majority")



def test():
    time_id = 2
    db = mongo_client.TestDb
    conversions_id = 'conversions_' + str(time_id)
    clicks_id = 'clicks_' + str(time_id)
    collection = db[conversions_id]

    pprint.pprint(collection.find_one())



