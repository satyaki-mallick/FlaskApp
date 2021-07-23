

import pprint
import pymongo

from pymongo import MongoClient
mongo_client = MongoClient("mongodb+srv://db-admin-satyaki:admin@cluster0.kkrlk.mongodb.net/Quarter_1?retryWrites=true&w"
                     "=majority")


def test():
    db = mongo_client.Quarter_2
    collection = db.conversions_2
    #pprint.pprint(collection.find_one())
