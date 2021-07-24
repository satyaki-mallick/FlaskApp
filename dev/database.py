

import pprint
import pymongo

from pymongo import MongoClient
mongo_client = MongoClient("mongodb+srv://db-admin-satyaki:admin@cluster0.kkrlk.mongodb.net/MyFirstDatabase?retryWrites=true&w"
                     "=majority")



def test():
    db = mongo_client.MyFirstDatabase
    collection = db.conversions_2
    #pprint.pprint(collection.find_one())




def access_banner():
    pass